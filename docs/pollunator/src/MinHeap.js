class MinHeap {
    constructor(capacity, getValueMethod){
        this.heapSize = -1;
        this.heap = Array(capacity).fill(-1)
        this.getValue = getValueMethod
    }
    
    insert(value){
        if(this.heapSize+1 === this.heap.length){
            throw Error("Overflow Size")
        }
        this.heap[this.heapSize + 1] = value
        this.heapSize = this.heapSize + 1
        this.siftUp(this.heapSize);
    }
    
    swap(i,j){
        [this.heap[i],this.heap[j]] = [this.heap[j],this.heap[i]]
    }
    
    siftDown(index){
        let minIndex = index
        let n = this.heap.length
        let lc = 2*index + 1
        if(lc<=n-1 && this.getValue(this.heap[lc]) < this.getValue(this.heap[minIndex]) ) minIndex=lc
        let rc = 2*index + 2
        if(rc<=n-1 && this.getValue(this.heap[lc]) < this.getValue(this.heap[minIndex]) ) minIndex=rc

        if(minIndex !== index){
            this.swap(index,minIndex)
            this.siftDown(minIndex)
        }
    }
    
    siftUp(index){
        let parent  = Math.ceil((index-1)/2)
        while(index>0 && this.getValue(this.heap[parent]) > this.getValue(this.heap[index]) ){
            this.swap(index,parent)
            index = parent
            parent = Math.ceil((index-1)/2)
        }
    }

    extractMin(){
        let result  = this.heap[0]
        this.heap[0] = this.heap[this.heapSize]
        this.heapSize = this.heapSize - 1
        this.siftDown(0)
        return result
    }

}

export default MinHeap