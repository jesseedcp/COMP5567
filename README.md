
# COMP 5567 区块链的分布式算法与协议

2025 秋季 项目说明（Project Specification） 

## 目标（Objective）

深入理解工作量证明（PoW）与权益证明（PoS）两类共识协议，包括其实现与安全性方面的考量。 

## 要求（Requirements）

本项目为分组完成（每组最多 6 人）。每位成员都应作出相对均衡的贡献。项目报告中必须包含工作量表与个人贡献清单。

注：若项目小组仅有 1–2 名成员，则可将整个项目聚焦于**单一**攻击场景。

项目分为两个主要部分：

1. PoW 51% 双花攻击（Double Spending Attack）
2. PoS 长程（Long-Range）攻击  

学生需要分别为上述两种场景实现**概念验证（PoC）代码**，并对源码做出**详细分析**，解释其 PoC 背后的运作机制。 

重要提示：项目**必须**基于所提供的基础代码完成；否则为防止抄袭，成绩将**扣减 80%**。

请使用你自己的语言撰写文档，并确保对使用的材料进行了适当引用（例如引用 ChatGPT 或外部代码）。请注意理大关于抄袭的手册：
[https://www.polyu.edu.hk/ogur/docdrive/Academic_Integrity/Plagiarism_Booklet.pdf](https://www.polyu.edu.hk/ogur/docdrive/Academic_Integrity/Plagiarism_Booklet.pdf) 

## 项目日程（Project Schedule）

* 演示（Demonstration）：2025 年 11 月 29 日 10:00–13:00，地点 Y306。
* 所有项目交付物提交：2025 年 12 月 2 日 23:59，于 Blackboard。
  逾期提交将被扣分，除非能提供合理说明。 

## 课程目标（Goals）

* 理解区块链系统的基础。
* 学习并实现 PoW 与 PoS 共识机制。
* 分析安全漏洞，尤其是 PoW 的双花与 PoS 的长程攻击。 

## 需要实现的组件（Components to Implement）

### 1) PoW 双花攻击（51% Attack）

* 实现一个在 PoW 网络上展示 51% 攻击的场景。
* 详细解释该攻击的具体过程及其影响。 

### 2) PoS 长程攻击（Long-Range Attack）

* 实现一个在 PoS 网络上模拟长程攻击的方案。
* 分析此类攻击对网络安全与共识的潜在影响。 

## 项目提交（Project Submissions）

* 项目汇报与演示：2025 年 11 月 29 日 10:00–13:00，地点 Y306（可由 2–3 名组员进行汇报）。
* 最终交付物（截止：**2024** 年 12 月 2 日 23:59，原文如此）：

  * 一份完整的小组报告（PDF 格式，页数不限），说明你们的实现与心得体会。凡非原创的材料或想法，务必正确引用。
  * 每位同学需提交一份**个人短报告**（最多半页），说明个人的贡献与职责。
  * 源代码：包含你们项目完整源码的文件夹。 

每组需提交单个压缩文件（.zip、.7z 等），以某位组员的姓名命名。**注意：最终提交需上传至 Blackboard。**
参考基础代码仓库：

1. [https://github.com/chainflag/ctf-blockchain](https://github.com/chainflag/ctf-blockchain) challenges/tree/main/public_blockchain/mini_blockchain/src
2. [https://github.com/goudanwang/miniblockchain2.git](https://github.com/goudanwang/miniblockchain2.git)   

## 评分方案（Grading Scheme）

本项目总分 15 分，另设加分项。评分细则如下： 

* **PoW 双花 PoC（4 分）**：在原型系统上可成功运行的源码。
* **PoS 长程攻击 PoC（4 分）**：在原型系统上可成功运行的源码。
* **系统集成（2 分）**：两种攻击的**完整演示视频**。
* **项目报告与展示（5 分）**：报告需包含两类漏洞原理说明、对原型系统代码的详细分析、以及两个 PoC 的具体说明。展示需讲解两类攻击并现场演示 PoC。
* **合计：15 分**。
* **加分项（+2 分）**：在所提供的实现上，修复与 PoC 对应的攻击路径。

## 演示（Presentation）

每组合计 10 分钟：

* 幻灯片讲解 4 分钟
* PoC 现场演示 4 分钟
* 问答 2 分钟 

## 备注（Notes）

* 请遵循理大的学术诚信与抄袭政策，确保正确引用与原创性。
* 与外部来源的代码相似度不得超过 10%（不含提供的基础代码）。 

## 资源（Resources）

鼓励参考学术论文、开源代码与相关文档来支持你们的实现与分析；请在报告中遵循适当的引用规范。 


