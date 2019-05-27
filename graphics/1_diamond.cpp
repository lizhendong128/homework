# 绘制金刚石程序
# vs2019创建的MFC工程
# 在view里的Ondraw()方法里进行实现
# 故代码只贴了相应的部分

void CTestView::OnDraw(CDC* pDC)
{
	CTestDoc* pDoc = GetDocument();
	ASSERT_VALID(pDoc);
	// TODO: add draw code for native data here

	CPoint p[32];
	double r = 400;
	int i,j;
	
	pDC->Ellipse(0,0,int(r*2),int(r*2));

	for(i=0;i<30;i++)
	{
		p[i].x=r*cos(i*3.14/15)+r;//计算正五边形顶点
		p[i].y=r*sin(i*3.14/15)+r;
	}
	
	for(i=0; i<30; i++)
		for(j=0; j<30; j++)
		{
			if(i!=j)
			{
				pDC->MoveTo(p[i].x, p[i].y);
				pDC->LineTo(p[j].x, p[j].y);
			}
		}
}
