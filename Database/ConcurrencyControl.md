## Schedule 이란?

트랜잭션을 나열하고 하나씩 실행하는 프로세스
동시에 실행되는 트랜잭션이 여러 개 있으면, 작업이 서로 겹치지 않도록 작업순서를 정함.

### Serial Schedule

먼저 실행중인 트랜잭션이 종료될 때까지 다음 트랜잭션이 시작되지 않음.

### Non Serial Schedule 

동시성 문제 발생 가능, 먼저 실행된 트랜잭션이 완료되기 전에 다음 트랜잭션이 수행될 수 있다.

* Serializable
	
    - Conflict Serializable
    - View Serializable

* Non-Serializable

---

## Serializable

DB의 일관성 유지. Non Serial Schedule에서 불일치가 존재하는지 확인하는데 사용

---

### Conflict Serializable

충돌하지 않는 작업을 교환(swapping)하여 Serializable할 수 있는 경우의 Schedule

#### Conflict Equivalence

Schedule S가 swapping을 통해 Schedule S' 가 될 수 있다면, S와 S'는 **Conflict Equivalence**라고 함.
#### 실행 순서의 중요성

Same data, different transactions, one of these instruction is write operation.

* li : a read or write instruction of Ti
* lj : a read or write instruction of Tj
* S : a schedule to include Ti and Tj


1. li = read(Q) and lj = read(Q)인 경우 : **실행 순서는 중요치 않음.**
2. li = read(Q) and lj = write(Q)인 경우 : **실행 순서가 중요함.**
3. li = write(Q) and lj = read(Q)인 경우 : **실행 순서가 중요함.**
4. li = write(Q) and lj = write(Q)인 경우 : **두 작업 이후에 read(Q)가 있다면 실행 순서 중요**

---

### View Serializable

Serial Schedule과 View Equivalent하다면, 그 Schedule은 View Serializability.

### View Equivalent
아래 조건들을 만족할 때, 두 스케쥴은 View Equivalent

1. **Initail Read**
	![https://www.javatpoint.com/dbms-view-serializability](https://velog.velcdn.com/images/hamkua/post/c1bd2550-88eb-4b0e-a026-6b6459efcd76/image.png)
    
    두 Schedule에서 Ti가 S에서 처음 읽는 값은 S'에서도 Ti가 처음 읽는 값이어야 한다.
    
2. **Updated Read**

	![https://www.javatpoint.com/dbms-view-serializability](https://velog.velcdn.com/images/hamkua/post/3acaaec9-458b-4f5f-88be-3599331307b0/image.png)

	S에서 Ti가 Tj에 의해 생성된 값을 읽는다면, S'에서도 Ti는 Tj에 의해 생성된 값을 읽어야 함.
    
3. **Final Write**
	
    ![https://www.javatpoint.com/dbms-view-serializability](https://velog.velcdn.com/images/hamkua/post/575b86b5-a4f7-4173-9b82-3bb1015351b7/image.png)

	the transaction that performs the final write(Q) operation in schedule S must perform the final write(Q) operation in schedule S.
    
---

## Serializability Test 

### Conflict Serializability Testing Mechanism

S = a Schedule 
G = (V, E) a precedence graph
	
* V = { T1, T2, T3, ... Tn } a set of nodes
* E = { e1, e2, e3, ... em } a set of directed edges
> edge e1은 Tj가 시작 노드이며 Tk가 마지막 노드인 Tj -> Tk의 형태이다. ei는 Tj에서 Tk사이에, Tj의 작업 중 Tk에서 충돌하기 전까지 작업중 하나가 schedule에 나타날 때 
 
 
예시:

1. Schedule에 참여하는 트랜잭션을 노드로 한다.

2. Conflicting operation인 read(X), write(X)에 대하여,
만약 Ti에서 write를 수행한 뒤에, Tj에서 read를 수행하는 경우 Ti와 Tj를 잇는 선을 그린다.

3. Conflicting operation인 write(X), read(X)에 대하여,
만약 Ti가 read를 수행한 뒤에, Tj에서 write를 수행하는 경우 Ti와 Tj를 잇는 선을 그린다.

4. Conflicting operation인 write(X), write(X)에 대하여,
만약 Ti가 write를 수행한 뒤에, Tj에서 write를 수행하는 경우 Ti와 Tj를 잇는 선을 그린다.

5. Schedule S는 precedence graph에서 **어떠한 사이클이 없기때문에, serializable하다.**

> 그래프에 어떠한 사이클도 없다는것은, conflict equivalent한 serial schedule S'를 생성할 수 있다는 것이다

예시2 :

Schedule S가 다음과 같을때, `S : r1(x) r1(y) w2(x) w1(x) r2(y) `

1. 트랜잭션에 대하여 노드를 두개 생성한다.
![https://www.geeksforgeeks.org/precedence-graph-for-testing-conflict-serializability-in-dbms/](https://velog.velcdn.com/images/hamkua/post/1b118ec6-083d-4b31-9a8d-31153ce6b679/image.png)

2. 충돌을 일으키는 두 수행 r1(x), w2(x)에 대하여, w2(x)이 수행되기 전에 r1(x)가 수행된다. T1에서 T2로 향하는 선을 그린다(edge).
![https://www.geeksforgeeks.org/precedence-graph-for-testing-conflict-serializability-in-dbms/](https://velog.velcdn.com/images/hamkua/post/6feb0b9e-9363-4642-bb70-fb4b333b90d7/image.png)

3. 충돌을 일으키는 두 수행 w2(x), w1(x)에 대하여, w1(x)가 수행되기 이전에 w2(x)가 수행된다. T2에서 T1으로 향하는 선을 그린다(edge)
![https://www.geeksforgeeks.org/precedence-graph-for-testing-conflict-serializability-in-dbms/](https://velog.velcdn.com/images/hamkua/post/4b1a29a5-66b6-4664-8f2e-f8f557245f2b/image.png)

**그래프에 사이클이 존재하므로, conflict serializable 하지 않다**는 것을 알 수 있다.

### View Serializability Testing Mechanism

View serializability는 schedule들이 View-Serializable한지 아닌지 여부를 결정하는 개념이다. 어떤 schedule이 Serial Schedule과 view equivalence를 가진다면, View-Serializable하다는 것을 기억하자.


Conflict Serializable하지 않더라도, 일관성에 문제가 발생할 수 있다.

예시 :

다음과 같은 Schedule (S1)에서, 

|T1|	T2|	T3|
|---|---|---|
|a=100 ||
|read(a) ||
||a=a-40|
||write(a) //60|
|a=a-40|||
|write(a) //20|||
|||a=a-20|
|||write(a) //0|


아래 그림은 사이클을 포함하므로, not conflict-serializable하지만,
그렇다고 해서 Serial Schedule에 대해서 equivalence한지, 아닌지 장담할 수 없다.
![](https://velog.velcdn.com/images/hamkua/post/5704bb22-24d0-4c29-b684-0822577e27eb/image.png)


예시 2 :
(S1')

|T1|T2|T3|
|---|---|---|
|a=100 ||
|read(a) //100 ||
||||
|a=a-40 |||
|write(a) //60 |||
||a=a-40 ||
||write(a) //20 ||
|||a=a-20 |
|||write(a) //0 |

아래 그림은 사이클을 포함하지 않아 Conflict-Serializable하지 않다,

![](https://velog.velcdn.com/images/hamkua/post/3d3a7678-d654-42ed-91ce-f7733de0039b/image.png)

conflict-serializable한 경우 다음 세 조건을 만족하는데...

1. Equivalent to a serial schedule,
2. Consistent,
3. And also a View-Serializable.


방법 예시 :

1. 두 트랜잭션 간 view Equvalence를 만족하는지, 만족한다면 다음단계로.
2. 두 트랜잭션이 Conflict Serializable한지, Non-Conflict Serializable한지 확인.
	
    * 만약 Conflict Serializable하다면, 반드시 View Serializable하다.

	* 하지만 Non-Conflict Serializable하다면, 다음 단계로.
    
3. 다음 조건 비교

	* 만약 blind write가 존재하지 않는다면, 그 Schedule은 non-View Serializable Schedule이다.
    > Blind write란? : write연산 이후에 read를 수행하지 않는다면, 그 write작업은 blind write라고 함.
    
    * blind write가 존재한다면, 그 Schedule은 view serializable할수도, 아닐수도 있다. 
    
4. precedence graph를 그려보자, 사이클이 없다면 그 Schedule은 View-Serializable하지 않다.
    




---
출처 : [geeksforgeeks](https://www.geeksforgeeks.org/precedence-graph-for-testing-conflict-serializability-in-dbms/) , [javatpoint](https://www.javatpoint.com/dbms-view-serializability)