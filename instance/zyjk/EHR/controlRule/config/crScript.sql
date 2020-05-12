declare @beginData varchar(50)  --开始时间
declare @endData varchar(50)    --结束时间
set @beginData ='1990-10-10'
set @endData ='2020-01-01'

declare @t11 table
(
    archiveNum varchar(2000),
  result varchar(100),
  ruleld varchar(100),
  examinationDate datetime NULL,
  TargetTable varchar(50)
)
declare @ruleCount int --规则的总数

begin
--1:先创建一张临时表,用于存储相关查询出来的规则内容
--创建临时表
declare @t table
(
num int,
RuleId nvarchar(50),
RuleSql varchar(1000),
IsInsert int,
TargetTable varchar(50)
)

insert @t 
SELECT Row_number() over(order by r.RuleId) num,r.RuleId,r.RuleSql,case when r.ContactTable='HrHealthCheckup' then 1
when r.TargetTable='HrHealthCheckup'then 1
else 0 end as 'IsInsert',r.TargetTable FROM HrRule r
left join HrRuleProps p
on r.RuleId = p.RuleId
where p.Enable =1 

declare @sqlFilter varchar(200)  
---'''+@para+'''
set @sqlFilter =''
--set @sqlFilter = ' and t1.CreateTime>='+''''+@beginData+''''+'and t1.UpdateTime<='+''''+@endData+''''
--print @sqlFilter
--print  't1.CreateTime>='+'"'+@beginData+ '"'+' and t1.UpdateTime<='+'"'+@endData+'"'

--2:将规则相关内容进行变更
update @t set RuleSql =Replace(Cast([RuleSql] as nvarchar(4000)),'%w',@sqlFilter)

--print @RuleSql
--select * from @t

--3:对相关内容进行查找(创建临时表将相关数据插入)
--创建临时表
declare @t1 table
(
num int,
RuleId nvarchar(50),
RuleSql varchar(1000)
)
declare @sqlTable table
(
RuleSql varchar(1000)
)

declare @i int  
set @i=1
declare @ruleSql varchar(2000)
DECLARE @number varchar(10)
DECLARE @ruleId varchar(100)
DECLARE @TargetTable varchar(100)


while @i<=(select count(*) from @t)
--while @i<50
begin 
   
  begin try
  select @ruleSql=RuleSql,@ruleId=RuleId,@number=IsInsert,@TargetTable=TargetTable  from @t where num = @i
  
  select @number=IsInsert from @t where num=@i
  
  if (@number=0)
  begin
  
    Insert into @t11(archiveNum,result) EXECUTE(@ruleSql)
    --UPDATE @t11 set TargetTable=@TargetTable where TargetTable is null
 
    END
     else
      begin
    Insert into @t11(archiveNum,examinationDate,result)  EXECUTE(@ruleSql)
   --UPDATE @t11 set TargetTable=@TargetTable where TargetTable is null
    
    end
    UPDATE @t11 set ruleld=@ruleId where ruleld is null
    
  
  end try
  begin catch
  --异常捕获内容放入异常日志表
  
  insert into dbo.HrCheckoutExceptionLog(ExceptionRemark,ExceptionMethod,CreateTime) 
  select ERROR_MESSAGE() as ErrorMessage,@ruleSql as sql语句,@beginData as CreateTime
  
  
  
  end catch
  
  set @i=@i +1 
end



insert into HrRuleRecord(RecordId,RecordTime,RuleId,examinationDate,ArchiveNum,ispass)
select newid() as RecordId,getdate() as RecordTime,T.ruleld, T.examinationDate, T.ArchiveNum,T.result from @t11 T 
WHERE T.result =1

BEGIN
with a1 as (
select a.archiveNum,a.result,b.TargetTable
from @t11 a, @t b  where a.ruleld=b.RuleId)
insert into dbo.HrArchivesResult(archiveNum,TargetTable,ispass,createtime)
select archiveNum,TargetTable,case when SUM(cast(result as int))=0 then 1 else 0 end as 'ispass',GETDATE() as createtime from a1 
group by archiveNum,TargetTable
--SELECT * FROM @t11
END
end