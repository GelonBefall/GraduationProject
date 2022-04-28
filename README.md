# My GraduationProject - 基于深度学习的蛋白质二级结构指定方法
  
## 使用本程序需要额外增加的文件夹：
    /materials/dssp/dssp_*  
    /materials/pdb/pdb_*  
    /materials/pickle/  
    /materials/rgb/  
    /production/  
可以直接运行initDirs.py自动生成本程序所需的文件夹。  
  
## 已完成工作
### 阶段一：读取pdb和dssp文件数据
    1.1、使用DSSPDSSPparser包的parser模块，读取某蛋白的dssp文件，并获取某蛋白的α-螺旋区间。  
        1.1.1、更新了自动查找dssp文件的功能，现在能够自动在多文件夹下找到dssp文件了。  
    1.2、使用biopython的PDB模块读取pdb文件。  
        1.2.1、能够自动通过API从PDB下载本地不存在的蛋白质了。  
    1.3、使用pymysql包连接数据库。  
    1.4、生成一个PDB文件中所有Cα原子之间的距离矩阵，并将该矩阵存入数据库。  
    1.5、计算出蛋白质的α-螺旋的特征信息（包括距离的区间、平均距离，距离的方差）并存入数据库。  
  
### 阶段二：绘制蛋白质的灰度距离矩阵图片
    2.1、设计每个像素的颜色代表的两个Cα原子之间的初始距离（调整中）。  
    2.2、采用2.1设计好的初始距离，根据1.3生成的蛋白质距离矩阵，生成灰度距离矩阵。  
    2.3、使用pypng，读取2.2生成的灰度距离矩阵，逐像素绘制蛋白质灰度距离矩阵。  
    2.4、使用pypng，读取1.4获取某蛋白的α-螺旋区间，以及2.2生成的灰度距离矩阵，切片逐像素绘制α-螺旋区间的灰度距离矩阵。  
  
### 阶段三：设计蛋白质二级结构指定算法
#### 1、设计原理：
    （1）、因为蛋白质距离矩阵矩阵以对角线为对称轴，所以处理图片时，可以只处理上半或者下半的数据。在本研究中，采用了距离矩阵的上半部分作为处理部分。  
    （2）、蛋白质距离矩阵中的每一个数值都有其意义，例如坐标（A，B）代表A号残基的Cα原子与B号残基的Cα原子之间的距离。因此，在蛋白质距离矩阵中，以对角线的平行线为研究对象。基于矩阵的对角线，每向上（或者向下）平移n条平行线时，在该条线上，每一个坐标（A，B），B与A的间隔的残基数量也为n。  
    （3）、因此，获取每一条线上的所有数据，也就获得了两两Cα残基之间的距离。提取其中的距离特征，就可以设计相关算法指定出该蛋白的二级结构。  
  
#### 2、算法设计：
（1）第一种算法  

    因为在两两Cα原子中，相隔连续三个残基以内时，Cα原子间的距离相对来说比较固定，所以只遍历三条对称线。  
    遍历单条对称线时，如果连续的多个像素格代表的距离接近，就将其加入α-螺旋候选区间。  
    下一条对称线只遍历上一条线算出的α-螺旋候选区间，将范围再缩小，最后输出指定的α-螺旋位置。  

（2）第二种算法  

    因为考虑到一个α-螺旋中间会可能出现弯折情况，所以认为连续两个以上不合规范的将色块认为不是α-螺旋的一部分，并将这些位置剔除掉。  
    收集并祛除了所有不符合规范的色块区间，留下的部分就是认为是α-螺旋。  
  
## 当前工作：
1、重新设计二种算法，拟提高正确率。  
2、拟采用深度学习方式，使用pytorch构建模型，通过训练找到合适的灰度距离区间，提高识别率。  