# =============================================================================
# PASTE-AND-RUN DIAGNOSTICS -- run before trusting the 139.8M-row join
# =============================================================================

# --- 1. Is the mapping 1:1? -------------------------------------------------
# If rows_ > vendor_events_, one VENDOREVENTID maps to several EVENTIDs and
# every account loss is being counted more than once.
print(pd.read_sql("""
SELECT COUNT(*) AS rows_,
       COUNT(DISTINCT VENDOREVENTID) AS vendor_events_,
       COUNT(DISTINCT EVENTID)       AS qbe_events_
FROM EVT.VENDOREVENTSMAP
WHERE HAZARDZONEID = 57 AND VENDORVERID = 33
""", engine_ref))

# and the same question asked of the joined mapping_df itself
dup = mapping_df.duplicated(subset=["SIMID", "VENDOREVENTID"]).sum()
print(f"duplicate (SIMID, VENDOREVENTID) in mapping_df: {dup:,}")
print(f"distinct SIMID in mapping_df: {mapping_df['SIMID'].nunique():,}")
print(f"mean sims per event: {len(mapping_df) / mapping_df['VENDOREVENTID'].nunique():.1f}")


# --- 2. Is the ELT unique on (id, eventid)? ---------------------------------
# PARTITIONID is NOT in your join condition. If this analysis partitions,
# rdm_accountstd fans out and staging_df is already duplicated before the merge.
print(pd.read_sql("""
SELECT COUNT(*) AS rows_, COUNT(DISTINCT PARTITIONID) AS partitions_
FROM DBO.RDM_ACCOUNT WHERE ANLSID = 112
""", engine_rdm))

dup_elt = staging_df.duplicated(subset=["id", "eventid"]).sum()
print(f"duplicate (id, eventid) in staging_df: {dup_elt:,}")
print(f"distinct accounts (id) under anlsid 112: {staging_df['id'].nunique():,}")


# --- 3. Does the expansion factor make sense? -------------------------------
# 139,810,313 / 6,552,281 = 21.3. That SHOULD equal the mean sims per event
# for the events the ELT actually touches. If it is materially higher, the
# excess is duplication, not occurrence.
matched = staging_df["eventid"].isin(set(mapping_df["VENDOREVENTID"]))
print(f"ELT rows with a mapping: {matched.sum():,} / {len(staging_df):,} "
      f"({matched.mean():.1%})")

expected = (mapping_df[mapping_df["VENDOREVENTID"].isin(set(staging_df['eventid']))]
            .groupby("VENDOREVENTID").size())
print(f"expected join rows = {int((staging_df['eventid'].map(expected).fillna(0)).sum()):,}")
print(f"actual join rows   = 139,810,313")
# these two must agree exactly. Any gap is duplication.
