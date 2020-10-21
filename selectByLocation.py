# selectByLocation.py
# coding:utf-8

import os
import arcpy

def GetFiles(path, suffix):
    fileList = list()
    for file in os.listdir(path):
        if os.path.splitext(file)[-1] == suffix: 
            fileList.append(os.path.join(path, file))
    return fileList


def selectByLocation(sourceLayer, targetLayer, methord, outFile):
    """
    methord: str
        "INTERSECT" —如果输入图层中的要素与某一选择要素相交，则会选择这些要素。这是默认设置。
        "CONTAINS" —如果输入图层中的要素包含某一选择要素，则会选择这些要素。
        "COMPLETELY_CONTAINS" —如果输入图层中的要素完全包含某一选择要素，则会选择这些要素。
        "CONTAINS_CLEMENTINI" —该空间关系产生的结果同 COMPLETELY_CONTAINS，但下列情况例
        外：如果选择要素完全位于输入要素的边界上（没有任何一部分完全位于里面或外面），则不会
        选择要素。Clementini 将边界面定义为用来分隔内部和外部的线，将线的边界定义为其端点，
        点的边界始终为空。
        "WITHIN" —如果输入图层中的要素在某一选择要素内，则会选择这些要素。
        "COMPLETELY_WITHIN" —如果输入图层中的要素完全位于或包含在某一选择要素内，则会选择这些要素。
        "WITHIN_CLEMENTINI" —结果同 WITHIN，但下述情况例外：如果输入图层中的要素完全位于选择图层
        中要素的边界上，则不会选择该要素。 Clementini 将边界面定义为用来分隔内部和外部的线，将线
        的边界定义为其端点，点的边界始终为空。
        "ARE_IDENTICAL_TO" —如果输入图层中的要素与某一选择要素相同（就几何而言），则会选择这些要素。
        "BOUNDARY_TOUCHES" —如果输入图层中要素的边界与某一选择要素接触，则会选择这些要素。如果输入要
        素为线或面，则输入要素的边界只能接触选择要素的边界，且输入要素的任何部分均不可跨越选择要素的
        边界。
        "HAVE_THEIR_CENTER_IN" —如果输入图层中要素的中心落在某一选择要素内，则会选择这些要素。要素中
        心的计算方式如下：对于面和多点，将使用几何的质心；对于线输入，则会使用几何的中点。
    """
    arcpy.SelectLayerByLocation_management(targetLayer, methord, sourceLayer, "", "NEW_SELECTION")
    count = arcpy.GetCount_management(targetLayer).getOutput(0)
    print "Get {} grid points.".format(count)
    arcpy.CopyFeatures_management(targetLayer, outFile)
    
    


def run():
    sourcePath = r"D:\data\china_grid\province_buffer"
    sourceSuffix = r".shp"
    targetFile = r"D:\data\china_grid\China_grid_points_info.shp"
    methord = r"WITHIN_CLEMENTINI"
    outPath = r"D:\data\china_grid\province_grid"
    arcpy.MakeFeatureLayer_management(targetFile, "targetLayer")
    targetCount = arcpy.GetCount_management("targetLayer").getOutput(0)
    print "targetLayer has {} grid points.".format(targetCount)
    fileList = GetFiles(sourcePath, sourceSuffix)
    for sourceFile in fileList:
        name = os.path.basename(sourceFile)
        print "Start select by file: {}.".format(name)
        outFile = os.path.join(outPath, name)
        arcpy.MakeFeatureLayer_management(sourceFile, "sourceLayer")
        selectByLocation("sourceLayer", "targetLayer", methord, outFile)
        arcpy.Delete_management("sourceLayer")
    arcpy.Delete_management("targetLayer")
    print "End of work!!!"


run()

    
