# 201803

## [15]The globalization of angel investments: Evidence across countries  

### 数据来源启示
* 本文的数据来源中提到的两种方式具有参考价值：1.Corporate and financing database；2.Venture capital-specific database **我们是否有条件在国内寻找类似的数据库，即在获得IT橘子数据库的基础上，找类似于中国证券投资基金协会平台上的数据。这里面还涉及到一个问题，即某几个投资机构合伙人成立的一些有限公司，如何筛查**

*

---

# 20180226

## JY的文献报告索引

### [1]The structure of the investment networks of venture capital firms

#### 主要价值
分析了风险投资机构关系网络的作用（并借此提出Resource Exchange Model ），同时依据所投企业创新程度的高低进行分类，对HIVCs和LIVCs网络进行对比。**VC通过链接交换的资源（三类）具有参考价值，Resource Exchange Model可能有参考价值（if 后期需要建立类似的模型）**

#### 数据来源
* 基于Bygrave, Timmons and Fast 1984年的工作  

* 来源于Thomson Reuters Venture Economics：contains 1501 portfolio companies & 464 venture capital firms that had invested in those companies between about 1966 and 1982  

* VC firms are classified in the following group:  
  * Top 61 firms* (in terms of the most investments in portfolio companies)  
    * Top 21 HIVCs  
    * Top 21 LIVCs

#### 主要方法
* 提出Resource Exchange Model

* 联合投资模型“Networking Model for Joint Investments by Venture Capital Firms”  

* 而后对该模型的connectedness、intensity、centrality进行了衡量，并根据实际情况做出可能的解释  

#### 主要结论
* the greater the uncertainty, the greater the degree of co-investing，即某一行业不确定性越高，这个行业的VC co-investing 的联系越多，**其与本课题提出的假设猜想：越知名/越high-level的VC，co-investing越密集，有一定出入**  

* VC 通过链接来交换资源，（其中Bygrave 1987年的一篇文章指出“the sharing of knowledge”是关键）资源的定义如下：
		1. opportunity to invest in a portfolio company
		2. the spreading of financial risk
		3. the sharing of knowledge.

*以上两个结论均涉及到这篇文献：Syndicated investments by venture capital firms: A networking perspective（1987年）*

---

### [2]Whom you know matters Venture capital networks and investment performance.

#### 主要价值
通过VC之间的关系网络（syndication relationship）来研究VC在网络中的重要性对VC表现的影响（其表现体现在两个方面：fund-level；portfolio-company-level），**其运用的方法具有较高的参考性，感觉是与本课题最相关的一篇文章**

#### 数据来源
* 数据来源于Thomson Financial’s Venture Economics database

* 选取了1980 – 2003 美国风险投资机构投资记录（实际是1980~1999发起的投资），去掉了angels and buyout funds

* 包含了1974家VC firms发起的3469个VC funds，进行了共计47705次 investment rounds，其中所投企业有16315家。（44.7%的 investment rounds 和 50.3%的企业为syndicated funding联合投资）

* 对“firm”和“fund”做了区分，其中firm会继承fund投资所获经验

#### 主要方法
* 构造VC 间的 syndication relationship 网络，移用了图论的相关研究方法
  * 两种方式定义syndicate（investment-round level；company level ）
  * 定义fund-level performance和company-level performance的量化指标
  * 量化 VC 的指标；量化VC experience的指标；等需要控制变量的variable，**其中有部分指标具有很强的相关性，未能提供很好的剔除方法**
  * 网络度量的限定，每5年为一个网络切片


* VC在网络中的重要性（Centrality）反应在5个方面，可以用Degree 、Closeness、Betweenness来量化；**个人感觉本课题在此基础上还可以利用InvestorRank、k-core值、聚类系数等量来补充说明**
> 知乎上有一篇博文介绍了根据各指标（Degree；Betweeness；最短路径；InvestorRank）对VC/基金进行排名，其榜单的差距不大

* VC表现反应在 ① 选择promising companies的能力 ② 为portfolio companies增值的能力，可以通过fund-level performance和company-level performance来量化

* 控制变量“fund characteristic”；“VC experience”*（More experience ≠ better VC network positions）* **（个人认为这个控制的必要性值得考究）**；“Competition for deal flow”；“Investment opportunities”，**整个这部分实验过程私以为很值得参考**

* 文中将portfolio companie按照产业分类，其分类标准为：biotechnology, communications and media, computer related, medical/health/life science, semiconductors/other electronics, and non-hightechnology，**私认为其对本课题挖掘国外数据有参考价值**

#### 主要结论
* 在VC网络中具有更central的位置的VC firms，有着更加的表现（both in fund-level & portfolio company-level）

* 通过这个网络中的关系，①特别是和well-networked的VC链接；②having access to other VC的deal flow *（通过邀请other VC into its syndicated，可以gain access to deal flow）*，VC firms收益最多

* Betweeness centrality（中介性）这一指标对于其performance的影响最小

#### 有价值的文献引用
* 文中再现Kaplan and Schoar’s 2005的研究fund performance model，其中提到的文献“Private equity returns: Persistence and capital flows”有一定参考价值

* 文中提到的syndicated VC deals联合投资带来更高的returns这一说法，值得考究 **（私以为联合投资在一定程度上也代表着VC在其网络中的centrality）**，相关文献“Venture‐capital syndication: Improved venture selection vs. the value‐added hypothesis”，引用次数很高，700多次

* **本文提到的VC network position来源的思路值得参考**

---
### [3]风险投资对上市公司投融资行为影响的实证研究

#### 主要价值
创新性的提出了讨论风投对于公司上市后阶段的作用影响，聚焦于投融资问题上（投资不足 & 过度投资），**其在论述风险投资对企业的影响具有参考价值，同时其对投资机构的特征进行分类也具有参考价值**

#### 数据来源
* 2002 – 2009；291 家风险投资机构和1384 家中国A 股上市公司（所有A股主板、中小板和创业板为初始样本，并作一定筛选）

* 通过分析上市公司十大股东，判断其是否具有风头背景 *（语义分析；查阅《中国创业投资发展报告》收录的风险投资名录；查询股东的主营业务）*

#### 主要方法
* 计量模型测算
  * 检验风险投资机构是否可以抑制自由现金流富余公司的过度投资 & 缓解内部现金流短缺公司的投资不足
      1. 投资过度与投资不足的程度
      2. 现金流与内部现金缺口
      3. 考察投资过度与自由现金流的关系&投资不足与现金缺口的关系

  * 检验风险投资机构对公司债务或权益融资的影响


#### 主要结论
* 风险投资加入上市公司的作用：
  1. 抑制公司对自由现金流的过度投资  
  2. 增加公司的短期有息债务融资和外部权益融资
  3. 在一定程度上缓解因现金流短缺所导致的投资不足

* 不同特征的风险投资机构对上述作用的影响有别：
  1. 高持股比例、高声誉、联合投资或非国有背景的风险投资机构的加入才可以显著地改善外部融资环境，缓解现金短缺公司的投资不足问题
  2. 几乎所有的风投机构都能抑制自由现金流过度投资的作用

#### 有价值的文献引用
* 风险投资对企业的影响（投融资方面）
  * 监督职能
  * 降低企业管理者与外部投资者之间的信息不对称 **（关系网络的信息传播功能）**
  * 有风险投资背景的企业公开上市时折价较少（基于前人研究）
  * 市场择机能力，帮企业在股市高峰进行IPO融资

* 根据风险投资机构的不同特征分类
  1. 持股比例
  2. 联合投资 *（关于联合投资对于公司正反两面影响的文献：Who are the active investors?: Evidence from venture capital 指出联合投资可能导致“搭便车”，不利于监督作用的发挥；Venture-Capital Syndication: Improved Venture Selection vs. The Value-Added Hypothesis 指出联合投资可以提供互补性管理经验；Whom you know matters: Venture capital networks and investment performance（已收录I期文献集）指出联合投资关系网络的信息传递功能能减少企业与资金提供者的信息不对称问题，促进外部融资）*
  3. 国有背景
  4. 声誉


---
### [8]The role of venture capital firms in Silicon Valley's complex innovation network

#### 主要价值
利用复杂网络理论分析了硅谷地区创新原动力，同时提出了VC在硅谷地区的经济网络为hub，有很大的贡献 **（可以为成都新经济的发展类型文章提供理论依据），VC在整个网络中发挥的作用具有参考价值（二部分图部分）；质疑的点，数据来源可信度和其主观性**

#### 数据来源
* Based on more than 40 non-directive interviews with entrepreneurs, venture capitalists, lawyers, journalists, consultants, bankers and professors in Silicon Valley, explores the interactions of VC firms with the other agents of Silicon Valley (为了发掘VC的贡献)

#### 主要方法
* 理论依据：复杂网络

* 硅谷的经济环境/网络符合复杂网络的定义
  * Network agents are heterogeneous and multiplex （with different competences and different functions）
  * Interactions of the network are multiplex and self-organized（社团结构&分级结构）
  * Robustness
  * 保持robustness的原因是其具有anticipating和learning能力（这部分能力主要来源于VC）

#### 主要结论
* 硅谷之所以能有源源不断的创新力，其主要原因在于其innovative cluster，即整体作为一个复杂网络的robustness很强（同时其也指出复杂网络中比较经典的关于一些重要的节点 “highly-connected node”被破坏而导致整个系统的摧毁问题）

* 针对VC在整个网络中所起到的作用进行一一分析
  * Financing
  * Selection
  * Signalling
  * Collective learning
  * Embedding

#### 有价值的文献引用
* 多次提到Barabasi的文章，**其中有“Scale-free network”和 “The structure and dynamics of network”个人感觉比较重要**
* “The Strength of Weak Ties”这篇文章引用很多，**同时其提出的弱关系感觉可以深挖迁移概念**
