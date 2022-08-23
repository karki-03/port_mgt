from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
import pandas as pd
import xlrd
import openpyxl
import csv
import os
from rest_framework import status
from .serializers import *
from django.conf import settings
from rest_framework.permissions import IsAuthenticated

""" 

APIView for saving the excel file, generating dump, tables and fields entries
Input: file, remarks
Output: Dump, table and fields data, for the uploaded excel file.

"""
class GenerateTables(APIView):
  parser_classes = [MultiPartParser, FormParser]
  permission_classes = (IsAuthenticated, )    
  def post(self, request, *args, **kwargs):
    file_serializer = FileSerializer(data=request.data)
    if file_serializer.is_valid():
      file_serializer.save()
      csv_path = file_serializer.data.get('file')

      file_name = csv_path.replace('/media/','')
      user_id = request.user
      original_file_directory = os.path.join(settings.MEDIA_ROOT,csv_path)
      print("user/owner:",request.user)
      #Make a dump table entry here
      #extract dump id from here
      dump_obj = Dump.objects.create(owner=user_id,original_file=original_file_directory,file_name=request.data.get('file'))
      if dump_obj:
        print("successfully dumped excel file")
        dump_id = dump_obj.id
        excel = openpyxl.load_workbook(request.data.get('file'))
        for worksheets in excel.sheetnames:
            worksheet = excel[worksheets]
            print(worksheet.title)
            #make entries for Table model, for each sheet here
            #(dump id, full file path, sample path, table name, fingerprint)
            table_obj = Table.objects.create(dump=dump_obj,delta_path=original_file_directory, table_name = worksheet.title)
            if table_obj:
                print("successfully made table from worksheet: " + worksheet.title)

                df = pd.read_excel(r'.'+csv_path,sheet_name=worksheet.title) #worksheet.values
                columns_dtype_dict = df.convert_dtypes().dtypes.to_dict()
                for key in columns_dtype_dict:
                  column_name = key
                  column_dtype = columns_dtype_dict[key]
                  field_obj = Field.objects.create(table=table_obj,dump=dump_obj,field_name=column_name, field_type = column_dtype)
                  if field_obj:
                      print("successfully made field ("+column_name+") from table: " + worksheet.title)
                      #make entries for field model, for each sheet here
                      # (table id, dump id, field name, field type, fingerprint)
                  else:
                      raise Exception("Something went wrong while uploading the worksheet fields ("+column_name+") in the table : Field")

                # for col in column_name_tuple:

                # df = pd.read_excel(file_name,sheetname=0,header=0) #,converters={'names':str,'ages':str}
                # print(df.dtypes)

                #make entries for field model, for each sheet here
                # (table id, dump id, field name, field type, fingerprint)+
               
            else:
                raise Exception('Something went wrong while uploading the worksheet in the table : Table')
      else:
        raise Exception('Something went wrong while uploading the file in the table : Dump')


      return Response(file_serializer.data, status=status.HTTP_201_CREATED)
    else:
      return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)