set identity_insert HrPersonBasicInfo ON
insert into HrPersonBasicInfo(ArchiveNum
,Name
,Sex
,DateOfBirth
,IdCard
,WorkUnit
,Phone
,ContactsName
,ContactsPhone
,ResidenceType
,NationCode
,BloodType
,RhBloodType
,Degree
,Occupation
,MaritalStatus
,HeredityHistoryFlag
,HeredityHistoryCode
,EnvironmentKitchenAeration
,EnvironmentFuelType
,EnvironmentWater
,EnvironmentToilet
,EnvironmentCorral
,DataSources
,CreateId
,CreateName
,CreateTime
,UpdateId
,UpdateName
,UpdateTime
,Status
,IsDeleted
,Version
,WorkStatus
,Telephone
,OccupationalDiseasesFlag
,OccupationalDiseasesWorkType
,OccupationalDiseasesWorkingYears
,DustName
,DustFlag
,RadioactiveMaterialName
,RadioactiveMaterialFlag
,ChemicalMaterialName
,ChemicalMaterialFlag
,OtherName
,OtherFlag
,PhysicsMaterialName
,PhysicsMaterialFlag
,DownloadStatus
,NoNumberProvided
,Id
) select ArchiveNum
,Name
,Sex
,DateOfBirth
,IdCard
,WorkUnit
,Phone
,ContactsName
,ContactsPhone
,ResidenceType
,NationCode
,BloodType
,RhBloodType
,Degree
,Occupation
,MaritalStatus
,HeredityHistoryFlag
,HeredityHistoryCode
,EnvironmentKitchenAeration
,EnvironmentFuelType
,EnvironmentWater
,EnvironmentToilet
,EnvironmentCorral
,DataSources
,CreateId
,CreateName
,CreateTime
,UpdateId
,UpdateName
,UpdateTime
,Status
,IsDeleted
,Version
,WorkStatus
,Telephone
,OccupationalDiseasesFlag
,OccupationalDiseasesWorkType
,OccupationalDiseasesWorkingYears
,DustName
,DustFlag
,RadioactiveMaterialName
,RadioactiveMaterialFlag
,ChemicalMaterialName
,ChemicalMaterialFlag
,OtherName
,OtherFlag
,PhysicsMaterialName
,PhysicsMaterialFlag
,DownloadStatus
,NoNumberProvided
,Id
 from healthrecord_test.dbo.HrPersonBasicInfo
where id=1231432 order by idcard desc