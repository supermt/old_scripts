CREATE TABLE NATION  ( N_NATIONKEY  int ,N_NAME CHAR(25) ,N_REGIONKEY  int ,N_COMMENT    VARCHAR(152));

CREATE TABLE REGION  ( R_REGIONKEY  int ,R_NAME CHAR(25) ,R_COMMENT    VARCHAR(152));

CREATE TABLE PART  ( P_PARTKEY     int , P_NAME  VARCHAR(55) , P_MFGR  CHAR(25) , P_BRAND CHAR(10) , P_TYPE  VARCHAR(25) , P_SIZE  int , P_CONTAINER   CHAR(10) , P_RETAILPRICE DECIMAL(15,2) , P_COMMENT     VARCHAR(23)  );

CREATE TABLE SUPPLIER ( S_SUPPKEY     int , S_NAME  CHAR(25) , S_ADDRESS     VARCHAR(40) , S_NATIONKEY   int , S_PHONE CHAR(15) , S_ACCTBAL     DECIMAL(15,2) , S_COMMENT     VARCHAR(101) );

CREATE TABLE PARTSUPP ( PS_PARTKEY     int , PS_SUPPKEY     int , PS_AVAILQTY    int , PS_SUPPLYCOST  DECIMAL(15,2)  , PS_COMMENT     VARCHAR(199)  );

CREATE TABLE CUSTOMER ( C_CUSTKEY     int , C_NAME  VARCHAR(25) , C_ADDRESS     VARCHAR(40) , C_NATIONKEY   int , C_PHONE CHAR(15) , C_ACCTBAL     DECIMAL(15,2)   , C_MKTSEGMENT  CHAR(10) , C_COMMENT     VARCHAR(117) );

CREATE TABLE ORDERS  ( O_ORDERKEY int ,  O_CUSTKEY  int ,  O_ORDERSTATUS    CHAR(1) ,  O_TOTALPRICE     DECIMAL(15,2) ,  O_ORDERDATE      DATE ,  O_ORDERPRIORITY  CHAR(15) ,  
  O_CLERK    CHAR(15) , 
  O_SHIPPRIORITY   int ,  O_COMMENT  VARCHAR(79) );

CREATE TABLE LINEITEM ( L_ORDERKEY    int , L_PARTKEY     int , L_SUPPKEY     int , L_LINENUMBER  int , L_QUANTITY    DECIMAL(15,2) , L_EXTENDEDPRICE  DECIMAL(15,2) , L_DISCOUNT    DECIMAL(15,2) , L_TAX   DECIMAL(15,2) , L_RETURNFLAG  CHAR(1) , L_LINESTATUS  CHAR(1) , L_SHIPDATE    DATE , L_COMMITDATE  DATE , L_RECEIPTDATE DATE , L_SHIPINSTRUCT CHAR(25) , L_SHIPMODE     CHAR(10) , L_COMMENT      VARCHAR(44) );
