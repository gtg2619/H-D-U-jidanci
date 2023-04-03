## 我爱记单词脚本

针对 [HDU平台](https://skl.hduhelp.com/#/call/course) 的我爱记单词脚本。平均分85。（每周题库不同，请使用前获取最新dictionary.txt）

键入`sessionId`及`WEEK`运行

```
python3 ./usgae.py
```

即可刷一次考试。

考试数据存放在`dictionary.txt`，可通过`getData.py`获取最新题目数据。

`getData.py`支持多个 Token 提高刷数据效率，需要更改 TIME 参数。

### 详细步骤

一、下载项目源码，选择 `Download Zip`并解压

<img src="README/image-20230403085509868.png" alt="image-20230403085509868" style="zoom:33%;" />

二、登录[杭电上课啦网页版平台](http://skl.hduhelp)

<img src="README/image-20230403084618012.png" alt="image-20230403084618012" style="zoom: 33%;" />

三、进入网页版`上课啦`界面

<img src="README/image-20230403084927777.png" alt="image-20230403084927777" style="zoom:33%;" />

四、打开控制台，输入 localStorage.sessionId ，回车。

<img src="README/image-20230403085150699-16804831149441.png" alt="image-20230403085150699" style="zoom:33%;" />

五、复制得到的字符串，粘贴到项目下的`usage.py`的对应位置。

<img src="README/image-20230403090213074.png" alt="image-20230403090213074" style="zoom:50%;" />

六、选择合适的参数

<img src="README/image-20230403090407747.png" alt="image-20230403090407747" style="zoom:50%;" />

七、运行脚本`python3 ./usage.py`。这个时候考试已经发起了

<img src="README/image-20230403091227741.png" alt="image-20230403091227741" style="zoom:33%;" />

八、等待脚本运行完成。等待的时间大概比设定的 TIME 值多一秒。结束即完成。
