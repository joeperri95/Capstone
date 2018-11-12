/**
************************************************************************
This sample is designed for the scenario which one input image contains 
one barcode, e.g. boarding pass, concert ticket, and various kinds of 
entrance tickets.
All settings are tuned to ensure the best efficiency under this scenario. 
Moreover, barcode format can be specified manually according to need.
*************************************************************************
*/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/time.h>
#include "../../../include/DynamsoftBarcodeReader.h"


int DecodeFile(CBarcodeReader& reader,const char* pszImageFile,int  iBarcodeFormat,float& fCostTime)
{
	struct timeval ullTimeBegin, ullTimeEnd;
	int iResult = 0;
    PublicRuntimeSettings tempParam;
    reader.GetRuntimeSettings(&tempParam);
    tempParam.mMaxBarcodesCount = 1;
	tempParam.mBarcodeFormatIds = iBarcodeFormat;
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

bool GetPath(char* pPath)
{
	char pszBuffer[512] = {0};
	int iExitFlag = 0;
	size_t iLen = 0;
	FILE* fp = NULL;
	while(1)
	{
		printf("\r\n>> Step 1: Input your image file's full path:\r\n");
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

const int GetBarcodeFormatId(int iIndex)
{
	switch(iIndex)
	{
	case 1:
		return BF_All;
	case 2:
		return BF_OneD;
	case 3:
		return BF_QR_CODE;
	case 4:
		return BF_CODE_39;
	case 5:
		return BF_CODE_128;
	case 6:
		return BF_CODE_93;
	case 7:
		return BF_CODABAR;
	case 8:
		return BF_ITF;
	case 9:
		return BF_INDUSTRIAL_25;
	case 10:
		return BF_EAN_13;
	case 11:
		return BF_EAN_8;
	case 12:
		return BF_UPC_A;
	case 13:
		return BF_UPC_E;
	case 14:
		return BF_PDF417;
	case 15:
		return BF_DATAMATRIX;
	case 16:
		return BF_AZTEC;
	default:
		return -1;
	}
}


bool SetBarcodeFormat(int* pBarcodeFormat)
{
	char pszBuffer[512] = {0};
	int iExitFlag = 0;
	size_t iLen = 0;
	int iIndex = 0;
	while(1)
	{
		printf("\r\n>> Step 2: Choose a number for the format(s) of your barcode image:\r\n");
		printf("   1: All\r\n");
		printf("   2: OneD\r\n");
		printf("   3: QR Code\r\n");
		printf("   4: Code 39\r\n");
		printf("   5: Code 128\r\n");
		printf("   6: Code 93\r\n");
		printf("   7: Codabar\r\n");
		printf("   8: Interleaved 2 of 5\r\n");
		printf("   9: Industrial 2 of 5\r\n");
		printf("   10: EAN-13\r\n");
		printf("   11: EAN-8\r\n");
		printf("   12: UPC-A\r\n");
		printf("   13: UPC-E\r\n");
		printf("   14: PDF417\r\n");
		printf("   15: DATAMATRIX\r\n");
		printf("   16: AZTEC\r\n");

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

			iIndex = atoi(pszBuffer);
			if(iIndex > 0 || iIndex < 16)
			{
				*pBarcodeFormat = GetBarcodeFormatId(iIndex);
				break;
			}
		}

		if(iExitFlag)
			break;

		printf("Please choose a valid number. \r\n");

	}
	return iExitFlag;
}

void OutputResult(CBarcodeReader& reader,int errorcode,float time,char*pszTextResult,int pszTextResultLength)
{
	char * pszTemp1 = NULL;
	char* pszTempResult = NULL;
	int iRet = errorcode;

	if (iRet != DBR_OK && iRet != DBRERR_LICENSE_EXPIRED && iRet != DBRERR_QR_LICENSE_INVALID &&
		iRet != DBRERR_1D_LICENSE_INVALID && iRet != DBRERR_PDF417_LICENSE_INVALID && iRet != DBRERR_DATAMATRIX_LICENSE_INVALID && iRet !=DBRERR_AZTEC_LICENSE_INVALID)
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
	const char* pszTemplateName = NULL;

	char pszImageFile[512] = {0};
	char pszSettingFile[512] = {0};
	int iRet = -1;

	int iExitFlag = 0;
	char szErrorMsg[256];
	float fCostTime = 0;
	int iBarcodeFormat = (int)BF_All;

	printf("*************************************************\r\n");
	printf("Welcome to Dynamsoft Barcode Reader Demo\r\n");
	printf("*************************************************\r\n");
	printf("Hints: Please input 'Q'or 'q' to quit the application.\r\n");

	CBarcodeReader reader;
	iRet = reader.InitLicense("t0068NQAAAHCnlh2IhwbYYCFETUrGJyZhFWMPxRcH6dyaNyx1B/Llmk04fnUBNOE8eJs4rEMxsrBTudtJNfvCmYkE6W8sibU=");

	if(iRet != DBR_OK)
	{
		printf("Error code: %d. Error message: %s\n", iRet, szErrorMsg);
		return -1;
	}

	while(1)
	{
        iExitFlag = GetPath(pszImageFile);
		if(iExitFlag)
			break;
        iExitFlag = SetBarcodeFormat(&iBarcodeFormat);
		if(iExitFlag)
			break;

		// Read barcode
        iRet = DecodeFile(reader,pszImageFile,iBarcodeFormat,fCostTime);
		// Output barcode result
        char * pszTextResult = NULL;
	    pszTextResult = (char*)malloc(8192);
		OutputResult(reader,iRet,fCostTime,pszTextResult,8192);
		printf(pszTextResult);
        free(pszTextResult);
	}
	return 0;
}

