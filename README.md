# GraduationProject
## 使用本程序需要额外增加的文件夹：
/materials/dssp/  
/materials/pdb/  
/materials/pickle/  
/materials/rgb/  
/production/  
  
## 已完成工作
1、使用pymysql连接数据库。  
2、使用biopython的PDB模块读取pdb文件。  
3、生成一个PDB文件中所有Cα原子之间的距离矩阵，并将其存入数据库。  
4、生成该矩阵的灰度图（修改中）。  
5、读取某蛋白的dssp文件。  
  
## 当前工作：
1、获取某蛋白的α螺旋区间，并找出其结构特征。 
2、输出平行于对角线的所有线的格子。也就是说，输出一个残基与第1……n个的距离。  
3、采集该距离中的信息，不断向下一层移动，筛选出可能为α螺旋的残基位置。  