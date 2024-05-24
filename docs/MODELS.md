# HempDB Models

### The models defining our database schema. This documentation is intended for developers

## Company

This is the main model representing the bulk of the data we store. Since the CMCI mainly collects data on companies, it only made sense to have Company be the main model. 

| Column            	| Description                                         	|
|-------------------	|-----------------------------------------------------	|
| SrcKey            	| Source Key - institution that created this entry    	|
| Name              	| Name of the Entity                                  	|
| Industry          	| Foreign Key Field - Choice of Industrial / Chemical 	|
| Status            	| Foregin Key Field - Choice of Active / Inactive     	|
| Grower            	| Foreign Key Field - Choice of Yes/No                	|
| Headquarters      	| Address of Headquarters (If available)              	|
| Address           	| Address of Business                                 	|
| Sales             	| Annual Revenue                                      	|
| Product           	| List of Products                                    	|
| City              	| Business City                                       	|
| State             	| Business State (US & Canada)                        	|
| Country           	| Business Country                                    	|
| Solutions         	| Many to Many field - Companies Solutions            	|
| Stakeholder Group 	| Stakeholder Group as defined by CMCI                	|
| Development Stage 	| Development Stage as defined by CMCI                	|
| Product Group     	| Product Group as defined by CMCI                    	|
| SAS Contact       	|                                                     	|
| Description       	| Description of the Company                          	|
| Pub/Priv          	|                                                     	|
| Ticker            	|                                                     	|
| Naics             	|                                                     	|
| Phone             	| Phone                                               	|
| Email             	| Email                                               	|
| Stakeholder       	|                                                     	|
| Principal         	|                                                     	|
| Founded           	| Year Founded                                        	|
| Employees         	| Number of Employees                                 	|
| ParentCompany     	| Parent Company                                      	|
| OnMarket          	|                                                     	|
| ProductName       	| Name of Product                                     	|
| SKU               	|                                                     	|
| Notes             	| Any Notes about the Company                         	|
| ProcessingFocus   	|                                                     	|
| FacilitySize      	|                                                     	|
| BiomassCap        	|                                                     	|
| ExtractionType    	|                                                     	|
| GMP               	|                                                     	|
| News              	| Any recent news or headlines                        	|
| Reviews           	| Public Reviews                                      	|

## PendingCompany

This is a duplicate of Company, but meant to hold companies that are awaiting approval by an admin. This table is intended to work in tandem with the PendingChange table

## PendingChange

This table holds information on all pending changes. This table serves as the data source for the "changes approval" feature that admins have access to. It displays all currently pending changes that need to be reviewed (approved or denied). Changes can be deletes (a company deletion), edits (a company edit), or a creation (company creation). 

| Column     	| Description                                                                                 	|
|------------	|---------------------------------------------------------------------------------------------	|
| CompanyID  	| ID of the PendingCompany (if type == edit, create) OR ID of the Company (if type == delete) 	|
| ChangeType 	| Type of Change Pending. One of edit, create, delete                                         	|
| editId     	| ID of company to be edited (if type == edit), else blank                                    	|

