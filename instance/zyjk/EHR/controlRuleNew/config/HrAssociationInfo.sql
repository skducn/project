set identity_insert HrAssociationInfo ON
insert into HrAssociationInfo(Id
,TableSource
,Pid
,AssociationType
,Code
,Msg
,OccurDate
,Orders
,sourceType
) select Id
,TableSource
,Pid
,AssociationType
,Code
,Msg
,OccurDate
,Orders
,sourceType
 from healthrecord_test.dbo.HrAssociationInfo
where pid=1
