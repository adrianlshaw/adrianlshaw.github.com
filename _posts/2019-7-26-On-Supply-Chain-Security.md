
>Reminder: these are all personal opinions and are not affiliated with any employer 


Supply chain security has been a long standing problem within the computer industry. And hardware companies have always cared. Not only do they want to make sure that customers receive [the genuine article](https://www.pcworld.com/article/262325/your_pc_may_come_with_malware_pre_installed.html), but they also want to make sure that their parts don’t appear in competitor products.

It’s never been a sexy enough topic to reach high enough to the desks of CEOs. What it really needed was a big exciting cover story like the [Supermicro BMC](https://www.bloomberg.com/news/features/2018-10-04/the-big-hack-how-china-used-a-tiny-chip-to-infiltrate-america-s-top-companies
) article from Bloomberg. It’s all the rage. Now many who need to talk about supply chain security are now talking about it. Whether you believe the story was true or not is simply irrelevant - it’s something everybody in this industry should be concerned about. 

### The challenge

It still stands that supply chain security is an enormously complex issue, one that has very little to do with technical problems. It’s multi-faceted, but predominantly about business relationships. And any solution to these problems will be measured by the costs of altering established practices. If you’re competing on price with cheap consumer hardware then adding a dollar of operational costs per unit may simply put you out of the market altogether. If you trade cost for time spent on the factory line, you still have a problem, because time is money. The longer a product takes to assemble then the more money you have to spend on the factory.

While I mentioned business relationships, it’s also about understanding what you want to protect and from who. Everybody has a different supply chain. They all use totally different procedures and are customised slowly over time to reach an optimum level of efficiency on the factory floor. Supply chains can be short or incredibly long, typically with multiple suppliers at each stage. Sometimes your product is even assembled on the same line as your competitor’s product. Due to these factors, there just isn’t a generic threat model that can universally be applied. If you try to make an abstract threat model you simply lose the level of detail that is necessary to reason about this problem. There are no real shortcuts here.

### Solutions with incentives

Assuming business arrangements are dandy, I believe the most effective way to secure the supply chain is to build a chain of trust. It’s a bit like a “zero-trust” network, you authenticate all firmware to ensure that they are from the expected suppliers and you authenticate peripherals like you would with network endpoints. It’s a tried and tested method in other domains. In order to authenticate something you need to already have metadata, which would need to be provisioned at the previous stage. If this can be achieved then this can provide some assurance that final products are genuine. To solve the issue of cloned or missing components, classical inventory tracking should be used (not going to mention databases or blockchains here!). It all sounds rather simple but it really isn’t because the world of business is messy. You need all your suppliers to be on board with the idea. Like all instances of a chain of trust, you must implicitly trust the very first part of the chain. If the actual chain is of length one then it may be difficult to not trust your factory. 

Security alone usually isn’t enough of an incentive. There needs to be an industry wide incentive to make this all hang together consistently. If a solution helps solve a business problem as well a security problem, then it’s likely to get more serious attention from business leaders. One main incentive is to shift liability in case a problem occurs. More problems in a supplier component result in more support costs and even recalls, which ultimately reduces profits. Some manufacturers already have the technical means of doing this. This can be measured. Alternatively, some may argue that potential repetitional damage due to poor security can be a good business reason to provide better security practices. But that risk is hard to measure or predict numbers, and in my opinion, only effective once you’ve got a valuable brand. 

### What next?

Since I don’t think generic threat models are possible here, someone can and should make best practice guidelines. But best practices can often be blindly overruled by real world constraints. Like many other security problems, the costs have to be understood as early as possible so they can be factored into planning.

There is hope:

* Big companies like Apple, Amazon and Google are increasingly investing in on-house development and reducing their dependencies on external suppliers. They are big targets for attackers and possibly have the most to lose from attacks.

* Component authentication standards are being worked on in [DMTF](https://www.dmtf.org/content/dmtf-releases-security-protocol-and-data-model-spdm-architecture-work-progress) and [PCIe](http://pcisig.com/pcie%C2%AE-component-authentication). Apple have been [trailblazers](https://support.apple.com/en-us/HT204566) beforehand and I hope these emerging standards are well adopted.

* There are plenty of solutions out there that you can use, but none 
seem to provide a full solution, due to heterogeneous deployment
models. The most promising one seems to be [SDO](https://www.intel.co.uk/content/www/uk/en/internet-of-things/secure-device-onboard.html). 

So, some relevant questions to ask:

* What do you need to protect from who and at which stage of the supply chain?
* Who do you trust and what do you trust them not to do?
* Does the factory have internet connectivity? And what if you need to change factory in the future?
* What’s the cost of altering the production line workflow and does it meet your security objectives? Is the cost acceptable?
* What’s the cost of a supply chain security failure and who pays for it?

Let's hope companies make the right trade offs (for a poor example, see the [Superfish fiasco](https://www.bbc.co.uk/news/technology-41179214)).

