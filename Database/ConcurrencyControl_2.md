# Lock-Based Protocol

Serializability를 보장

## 1. Locks protocol

문제점 - 데이터 불일치가 발생할 수 있음.

### two made lock:
*  Shared mode : 만약 트랜잭션 Ti가 data item인 Q에 대해 shared mode lock이라면, 
Ti는 Q에 대해 read 연산만 가능하다. (write 불가)

* Exclusive mode : 만약 트랜잭션 Ti가 data item인 Q에 대해 exclusive mode lock이라면, 
Ti는 Q에 대해 read, write연산 둘 다 가능하다.

#### lock을 다루는 명령

* lock-S(Q) : 트랜잭션 T가 data item Q에 대한 shared-lock 요청, Q가 unlocked 상태인 경우 T에 의해 shared-mode로 lock 됨.

* lock-X(Q) : 트랜잭션 T가 data item Q에 대한 exclusive-lock 요청, Q가 unlocked 상태인 경우 T에 의해 exclusive-mode로 lock 됨.

* unlock(Q) : 트랜잭션 T가 점유(lock)하고있는 data item Q에 대한 lock-mode를 해제.

### Lock compatibility matrix

![https://www.geeksforgeeks.org/lock-based-concurrency-control-protocol-in-dbms/](blob:https://velog.io/06e15d54-ce66-40e3-8aae-9c94ad80cc0a)

어느 트랜잭션이 data item Q에 대해 exclusive lock을 가질 때, 이것을 unlock하기 전까지, 다른 트랜잭션에서는 어떠한 lock mode를 가질 수 없다. -> wait 해야 함.

예시 : 초깃값 A = 100, B = 200일 때,

![](https://velog.velcdn.com/images/hamkua/post/f60a9d31-00d4-4878-bc95-a25b0d0a64f5/image.png)


결과는 300이 아닌 250이 display된다. 
T7에서 data item B에 대한 unlock이 너무 빨리 수행되었기 때문이다.
이 문제를 해결하기 위해서는 각 트랜잭션의 unlock연산들을 맨 뒤로 위치시키는 방법이 있을 수 있다. (deadlock 발생 가능)

![](https://velog.velcdn.com/images/hamkua/post/497464c2-24e2-4494-8faf-ab22686239db/image.png)

하지만 T8에서 data item B에 대한 shared-mode를 요청하고, 이후의 작업이 수행되려면 T9에서 B에 대하여 unlock해 주어야 하고, 반대로 T9에서는 이후의 작업을 수행하려면 T10에서 A에 대해 unlock을 해 주어야 한다.
서로 wait 상태를 유지하고 작업이 정상적으로 수행되지 않는다.

![https://ecomputernotes.com/database-system/rdbms/type-of-lock-in-dbms#Types_of_Locks](https://velog.velcdn.com/images/hamkua/post/96644d14-89ac-4e02-9beb-7a747b7ee43f/image.png)

---

## 2. 2-Phase Locking Protocol

conflict serializability를 보장하지만, 이것 또한 deadlock이 발생할 수 있다.

### 2-Phase Locking

* Growing phase : 트랜잭션은 lock을 얻기만 하고, lock을 해제할 수 없다.
* Shrinking phase : 트랜잭션은 lock을 해제하기만 하고, lock을 얻을 수 없다.

### 2-Phase Locking 실행 순서

Growing phase -> 점유한 data item 사용 -> Shrinking phase -> Termination

### upgrade, downgrade 변환

* upgrade(Q) : shared-mode lock을 exclusive-mode lock으로 변환
* downgrade(Q) : exclusive-mode lock을 shared-mode lock으로 변환

---

## 3. Graph-Based Protocol 

conflict serializability를 보장 , deadlock-free
two-phase locking보다 concurrency degree를 증가시킴.

### Tree protocol
data item은 아무때나 unlock될 수 있음.
트랜잭션 T에 의해 lock된 이후에 unlock된 data item은 relock될 수 없음.

---

출처 : [geeksforgeeks](https://www.geeksforgeeks.org/lock-based-concurrency-control-protocol-in-dbms/) , [computernotes](https://ecomputernotes.com/database-system/rdbms/type-of-lock-in-dbms#Types_of_Locks)