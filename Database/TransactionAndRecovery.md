## Transaction Model 

### Transaction 이란?
여러 데이터 아이템들을 접근 또는 업데이트하기위한 단위.
트랜잭션은 데이터베이스의 일관성을 유지하도록 해야 한다.

### Transaction Abort 
Transaction의 성공적 실행의 실패.
abort되었을때, transaction의 중간 결과는 DB에 반영되면 안됨.

> rollback이란?  transaction abort발생시 그 transaction 수행 이전 상태로 되돌리는 작업

### Transaction Commit
Transaction의 성공적 실행 성공.
DB를 새로운 상태로 변경할 수 있음.

### Transaction State

![https://ecomputernotes.com/database-system/rdbms/transaction#States_of_Transaction](https://velog.velcdn.com/images/hamkua/post/7bb4db2a-2a82-4f6e-8b19-4ea6e2fe4ff3/image.png)

* **Active** : 실행 상태
* **Partially Commited** : transaction의 마지막 명령어 처리 수행(abort될 수 있음, 변경 내용을 DB에 반영하지 않은 상태)
* **Failed** : 정상 실행이 불가능
* **Aborted** : rollback을 통해 transaction의 실행 이전 상태로 되돌린 상태
* **Committed** : 마지막 명령어 처리 수행(변경 내용을 DB에 반영한 상태)

> **partially committed 상태와 committed 상태의 차이점**
[스택오버플로우](https://stackoverflow.com/questions/40815921/what-is-the-difference-between-partially-commited-and-commited-state-in-transact)
partially committed 상태는 트랜잭션의 모든 요소들이 수행되었을때, 발생한다. 
그리고 RDBMS가 데이터베이스의 변화를 유지하기위해서 논리적으로는 커밋했지만 실제적으로는 그것들이 반영되지 않았을 때를 의미한다.
"논리적으로"의 의미는 트랜잭션의 작업들이 수행된 이후에 여전히 실패할 가능성이 존재하기 때문이다. 이 실패 가능성 때문에, RDBMS는 이후에 실패가 발생할지라도 다시 복구하거나 업데이트 할 수 있도록 disk에 충분한 정보를 기록한다

---

## Recovery Mechanisms 

### Log-Based Recovery Mechanism

### Database Log(Journal) 
Log는 stable storage에 위치.
Log record로 구성됨( Log Record는 하나의 DB write연산을 나타냄, Log는 데이터베이스의 모든 갱신 작업을 기록한다. )

#### Log Record의 fields
* Transaction Name 
* Data item Name
* Data item의 old value 
* Data item의 new value 

#### Redo, Undo 차이점
Redo는 복구 시 이미 했던 작업을 그대로 다시 처리함. 
Undo는 이전의 작업을 반대로 진행.


### Deferred Database Modification
모든 DB의 변경들은 Log로 반영하는데, write에 의한 DB변경은 Partially Commit 이후로 지연시킨다. 
Partially Commit 이후, Write에 의한 변경 내용을 DB로 반영시킴.
이 작업은 Redo를 사용.
> The DB modification is deferred or delayed until the last operation of transaction is executed.

### Immediate Database Modification
데이터베이스 변경이 트랜잭션이 아직 실행중일 때 발생하는 경우, 사용된다.
데이터베이스는 매 작업 이후로 즉시 변경된다.( 트랜잭션이 Active 상태일 때, 변경사항을 DB에 반영 가능하게 함) 
> If the system crash or transaction aborts, 
then the old value field of the log records is used to restore the modified data items to the value they had prior to start of the transaction.( 이 작업은 Undo를 사용 ) 


---
## Buffer Management

### Log Record Buffering
1. 평상시 Log record를 main memory로 buffering.
2. main memory의 data block이 DB로 반영되기 직전에, 그 block data와 관련된 모든 Log record들을 Log file로 기록.
3. Log record가 Log로 출력되기 전에, 그 트랜잭션에 관련한 모든 Log record들을 Log로 출력.
4. Log record가 출력된 이후, 트랜잭션은 Commit상태가 됨.


### Database Buffering
Virtual Memory기법을 쓰는 시스템의 경우, Page fault가 발생!
> **Page fault**란? 프로그램이 자신의 주소 공간에는 존재하지만, RAM에는 없는 데이터에 접근을 시도했을 경우 발생.

Block B1을 swap-out하고, Block B2를 swap-in해야 할 경우
1. Block B1에 관련된 모든 Log record를 Log file에 기록.
2. Block B1을 DB로 출력.
3. Block B2를 DB에서 main memory(RAM)으로 가져옴.

> **swap-out** : RAM에 위치하는 데이터를 보조기억장치(Hdd, ssd)에 저장
**swap-in** : 반대로 보조기억장치에서 RAM으로 가져오는 것

### Checkpoint Mechanism
1. main memory에 존재하는 모든 Log record들을 Log file에 기록.
2. 변경된 모든 buffer block들을 DB로 출력.
3. checkpoint record를 Log file에 기록.

### Shadow Paging Mechanism
Page, Memory Frames, Page table을 갖는 Paging기법을 사용하는 시스템에서 이용.
> **Paging 기법**이란 ? :  가상 메모리(Virtual Memory)에서는 현재 이용하려는 데이터 전부를 가지고있지 않는다.
데이터가 저장되어있는 시작 주소값을 사용하는 방법은, 연속된 메모리공간 확보가 어렵다. Paging 기법은, 데이터의 물리적 주소공간이 연속되지 않아도 되는 메모리 관리 기법이다.

> **Page Table** : 가상주소를 물리적 주소로 바꾸어주기 위한 Table
**Memory Frame** : 메모리를 Frame이라는 것으로 분할한 것
**Pages** : 프로세스를 Page로 구분하여 분할한 것

**current page table**과, **shadow page table**을 이용한다.
![https://www.geeksforgeeks.org/shadow-paging-dbms/](https://velog.velcdn.com/images/hamkua/post/762b6d77-3d02-4dfb-9f20-7adffdc1e259/image.png)

current page table은 실행 중 변경될 수 있다. 반면에 shadow page table은 변경되지 않는 것을 알 수 있다.

#### Commit Operation
트랜잭션을 커밋하는 데에는 순서가 아래와 같다.

1. transaction에 의해 변경된 Buffer pages들을 Physical database로 출력.

2. current page table을 disk로 출력

3. current page table의 disk address를 shadow page table의 address를 포함하는 stable storage에 overwrite한다. 
(이 작업 이후, **current page table == shadow page table**)

---

[Transaction State 이미지 출처](https://ecomputernotes.com/database-system/rdbms/transaction#States_of_Transaction)
[Shadow paging mechanism 이미지 출처](https://www.geeksforgeeks.org/shadow-paging-dbms/)