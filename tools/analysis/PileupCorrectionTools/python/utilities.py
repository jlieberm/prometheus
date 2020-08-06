

__all__ = ["RetrieveBinningIdx"]


def RetrieveBinningIdx(et,eta,etbins,etabins, logger=None):
  # Fix eta value if > 2.5
  if eta > etabins[-1]:  eta = etabins[-1]
  if et > etbins[-1]:  et = etbins[-1]
  ### Loop over binnings
  for etBinIdx in range(len(etbins)-1):
    if et >= etbins[etBinIdx] and  et < etbins[etBinIdx+1]:
      for etaBinIdx in range(len(etabins)-1):
        if eta >= etabins[etaBinIdx] and eta < etabins[etaBinIdx+1]:
          return etBinIdx, etaBinIdx
  #if logger:  logger.warning('Can not retrieve the correct et (%1.3f)/eta (%1.3f) idx.',et,eta)
  return -1, -1



