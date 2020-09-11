var chooseDepartment = {
    props: ['departments', 'selected'],
    data: function(){
        return {
            initSelect: this.selected
        }
    },
    watch: {
        'selected': function(){
            this.initSelect = this.selected
        },
        'initSelect': function(){
            this.$emit("selectok", this.initSelect)
        }
    },
    template: `
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
    `,
}