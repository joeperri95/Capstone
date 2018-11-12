/**
************************************************************************
This C++ sample is developed using the C++ API of Dynamsoft Barcode Reader.
The sample demonstrates how to read barcode from the Linux Command Line.
*************************************************************************
*/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/time.h>
#include "../../../include/DynamsoftBarcodeReader.h"

int DecodeFile(CBarcodeReader& reader,const char* pszImageFile,float& fCostTime)
{
	struct timeval ullTimeBegin, ullTimeEnd;
	int iResult = 0;
    gettimeofday(&ullTimeBegin, NULL);
    iResult = reader.DecodeFile(pszImageFile);
    gettimeofday(&ullTimeEnd, NULL);
    fCostTime = (float)((ullTimeEnd.tv_sec * 1000 * 1000 +  ullTimeEnd.tv_usec) - (ullTimeBegin.tv_sec * 1000 * 1000 + ullTimeBegin.tv_usec))/(1000 * 1000);
    return iResult;
}

void ToHexString(unsigned char* pSrc, int iLen, char* pDest)
{
	const char HEXCHARS[16] = { '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F' };
	int i;
	char* ptr = pDest;
	for(i = 0; i < iLen; ++i)
	{
		//snprintf(ptr, 4, "%c%c ", HEXCHARS[ ( pSrc[i] & 0xF0 ) >> 4 ], HEXCHARS[ ( pSrc[i] & 0x0F ) >> 0 ]);
		ptr += 3;
	}
}

void OutputResult(CBarcodeReader& reader,int errorcode,float time,char*pszTextResult,int pszTextResultLength)
{
	char * pszTemp1 = NULL;
	char* pszTempResult = NULL;
	int iRet = errorcode;

	if (iRet != DBR_OK && iRet != DBRERR_LICENSE_EXPIRED && iRet != DBRERR_QR_LICENSE_INVALID &&
		iRet != DBRERR_1D_LICENSE_INVALID && iRet != DBRERR_PDF417_LICENSE_INVALID && iRet != DBRERR_DATAMATRIX_LICENSE_INVALID && iRet != DBRERR_AZTEC_LICENSE_INVALID)
	{
		snprintf(pszTextResult, pszTextResultLength, "Failed to read barcode: %s\r\n", CBarcodeReader::GetErrorString(iRet));
		return;
	}

	STextResultArray *paryResult = NULL;
	reader.GetAllTextResults(&paryResult);

	if (paryResult->nResultsCount == 0)
	{
		//snprintf(pszTextResult, pszTextResultLength, "No barcode found. Total time spent: %.3f seconds.\r\n", time);
		CBarcodeReader::FreeTextResults(&paryResult);
		return;
	}

	snprintf(pszTextResult, pszTextResultLength, "");
	for (int iIndex = 0; iIndex < paryResult->nResultsCount; iIndex++)
	{
		pszTempResult = (char*)malloc(4096);
		pszTemp1 = (char*)malloc(paryResult->ppResults[iIndex]->nBarcodeBytesLength*3 + 1);
		ToHexString(paryResult->ppResults[iIndex]->pBarcodeBytes, paryResult->ppResults[iIndex]->nBarcodeBytesLength, pszTemp1);
		snprintf(pszTempResult,2048,"%s",paryResult->ppResults[iIndex]->pszBarcodeText);

		strcat(pszTextResult,pszTempResult);
		free(pszTempResult);
		free(pszTemp1);
	}

	CBarcodeReader::FreeTextResults(&paryResult);
	return;
}

int main(int argc, const char* argv[])
{
	int iRet = -1;
	int iExitFlag = 0;
	char szErrorMsg[256];
	float fCostTime = 0;


	CBarcodeReader reader;
	reader.InitLicense("t0068NQAAACJdDFxMpfWIXH8s0ZFMF4nIRHs08zjq/710YcnXyB8+f1ZfpaSuRMPnqU7mwq3dJ0LUc/62rvCNnsSCxQOgzgQ=");


    // read barcode.
    const char* pszImageFile = NULL;
	if(argc<=1)
	{
		printf("Usage: ReadBarcode [ImageFilePath]\n");
		return 1; 
	}
	pszImageFile = argv[1];
    iRet = DecodeFile(reader,pszImageFile,fCostTime);
    if(iRet !=DBR_OK)
    {
        printf("Error code: %d. Error message: %s\n", iRet, szErrorMsg);
    }
    // output barcode result.
    char * pszTextResult = NULL;
    pszTextResult = (char*)malloc(8192);
    OutputResult(reader,iRet,fCostTime,pszTextResult,8192);
    printf(pszTextResult);
    free(pszTextResult);
	return 0;
}
