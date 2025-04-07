this repo has a solution of below mentioned problem statement:

Build a  document extraction solution that intelligently extracts data from Bills of Exchange, Goods Receipt Notes (GRNs), and Purchase Orders (POs). Using LLMs and vision models, it dynamically determines relevant fields based on QA pairs found in each document, ensuring adaptive extraction. i.e. if new fields are found, the extractor should extract name and value for the new field too.
 
Sample Fields per Document Type:
 
Bill of Exchange: Drawer, Drawee, Amount, Due Date, Acceptance Status.
Goods Receipt Note (GRN): Supplier Name, GRN Number, Received Items, Quantity, Inspection Status.
Purchase Order (PO): PO Number, Buyer Name, Supplier, Item List, Total Cost, Payment Terms.
Please find samples on the internet to create this demo.
