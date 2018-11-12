/**
*******************************************************************************
This sample is designed for the scenario in which the input images contain 
multiple barcodes.
All the settings are tuned to maximize number of successfully decoded barcodes.
*******************************************************************************
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
    PublicRuntimeSettings tempParam;
    reader.GetRuntimeSettings(&tempParam);
    
	// Set the expected barcodes count to the maximal value. 
	tempParam.mExpectedBarcodesCount = 0x7fffffff; 
    
	char error[1024] ={0};
    iResult = reader.UpdateRuntimeSettings(&tempParam,error,1024);
    if(iResult != DBR_OK)
	{
		printf("Error code: %d. Error message: %s\n", iResult, error);
		return iResult ;
	}
    gettimeofday(&ullTimeBegin, NULL);
    iResult = reader.DecodeFile(pszImageFile);
    gettimeofday(&ullTimeEnd, NULL);
    fCostTime = (float)((ullTimeEnd.tv_sec * 1000 * 1000 +  ullTimeEnd.tv_usec) - (ullTimeBegin.tv_sec * 1000 * 1000 + ullTimeBegin.tv_usec))/(1000 * 1000);
    return iResult;
}


bool GetPath(char* pPath,bool bIfImagePath)
{
	char pszBuffer[512] = {0};
	int iExitFlag = 0;
	size_t iLen = 0;
	FILE* fp = NULL;
	while(1)
	{
		if(bIfImagePath)
		{
			printf("\r\n>> Step 1: Input your image file's full path:\r\n");
		}else
		{
			printf("\r\n>> Step 1: Input your template file's full path:\r\n");
		}

		fgets(pszBuffer,512,stdin);

		iLen = strlen(pszBuffer);

		if(iLen > 0)
		{
		   	pszBuffer[iLen -1] ='\0';

			if(strlen(pszBuffer) == 1 && (pszBuffer[0] == 'q' || pszBuffer[0] == 'Q'))
			{
				iExitFlag = 1;
				break;
			}

			memset(pPath, 0, 512);
			if(pszBuffer[0]=='\"' && pszBuffer[iLen-1] == '\"')
				memcpy(pPath, &pszBuffer[1], iLen-2);
			else
				memcpy(pPath, pszBuffer, iLen);
			fp = fopen(pPath, "rb");
			if(fp != NULL)
			{
				fclose(fp);
				break;
			}
		}
		printf("Please input a valid path.\r\n");
	}
	return iExitFlag;
}


void ToHexString(unsigned char* pSrc, int iLen, char* pDest)
{
	const char HEXCHARS[16] = { '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F' };

	int i;
	char* ptr = pDest;

	for(i = 0; i < iLen; ++i)
	{
		snprintf(ptr, 4, "%c%c ", HEXCHARS[ ( pSrc[i] & 0xF0 ) >> 4 ], HEXCHARS[ ( pSrc[i] & 0x0F ) >> 0 ]);
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
		snprintf(pszTextResult, pszTextResultLength, "No barcode found. Total time spent: %.3f seconds.\r\n", time);
		CBarcodeReader::FreeTextResults(&paryResult);
		return;
	}

	snprintf(pszTextResult, pszTextResultLength, "Total barcode(s) found: %d. Total time spent: %.3f seconds\r\n\r\n", paryResult->nResultsCount, time);
	for (int iIndex = 0; iIndex < paryResult->nResultsCount; iIndex++)
	{
		pszTempResult = (char*)malloc(4096);
		pszTemp1 = (char*)malloc(paryResult->ppResults[iIndex]->nBarcodeBytesLength*3 + 1);
		ToHexString(paryResult->ppResults[iIndex]->pBarcodeBytes, paryResult->ppResults[iIndex]->nBarcodeBytesLength, pszTemp1);
		snprintf(pszTempResult,2048,"Barcode %d:\r\n    Type: %s\r\n    Value: %s\r\n    Hex Data: %s\r\n",iIndex + 1,paryResult->ppResults[iIndex]->pszBarcodeFormatString,paryResult->ppResults[iIndex]->pszBarcodeText,pszTemp1);

		strcat(pszTextResult,pszTempResult);
		free(pszTempResult);
		free(pszTemp1);
	}

	CBarcodeReader::FreeTextResults(&paryResult);
	return;
}

int main(int argc, const char* argv[])
{
	char pszImageFile[512] = {0};
	int iRet = -1;

	int iExitFlag = 0;
	float fCostTime = 0;

	printf("*************************************************\r\n");
	printf("Welcome to Dynamsoft Barcode Reader Demo\r\n");
	printf("*************************************************\r\n");
	printf("Hints: Please input 'Q'or 'q' to quit the application.\r\n");

	CBarcodeReader reader;
	reader.InitLicense("t0068NQAAABz2TdBAk3vZRLWyKrDDImistF3vB616xdLTapjH3mP0RljfaQyqbvh0t5kmO33/3YjxXZK/jTAJ+PnzgS3/bEM=");

	while(1)
	{
        iExitFlag = GetPath(pszImageFile,true);
		if(iExitFlag)
			break;

		// Read barcode
        iRet = DecodeFile(reader,pszImageFile,fCostTime);
		// Output barcode result
        char * pszTextResult = NULL;
	    pszTextResult = (char*)malloc(8192);
		OutputResult(reader,iRet,fCostTime,pszTextResult,8192);
		printf(pszTextResult);
        free(pszTextResult);
	}
	return 0;
}

