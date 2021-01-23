var chooseDepartment = {
    props: ['departments', 'selected'],
    data: function(){
        return {
            initSelect: this.selected,
            initFounded: "",
        }
    },
    watch: {
        'selected': function(){
            this.initSelect = this.selected
        },
        'initSelect': function(){
            this.$emit("selectok", this.initSelect)
        },
        'initFounded': function(){
            this.$emit("foundedok", this.initFounded)
        }
    },
    template: `
    
    <div class="mx-auto">
        <div>
            <h5>1. 「課程名稱」直接搜尋</h5>
            <input class="form-control" type='text' v-model='initFounded'>
        </div>
        <div class="text-center my-2">
            <h5>或</h5>
        </div>
        <div>
            <h5>1. 選擇類別</h5>
            <select class="custom-select mr-sm-2" v-model="initSelect">
                <option v-for="(item, index) in departments" :key="index" 
                    v-bind:value="item"
                >
                    {{ item }}
                </option>
            </select>
        </div>
    </div>
    `,
}