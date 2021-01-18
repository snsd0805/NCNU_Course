var share = {
    data: function(){
        return {
            'selectCourses': [],
        }
    },
    mounted() {
        this.getCourses()
    },
    components: {
        'course-table': courseTable,
        'choose-department': chooseDepartment,
        'course-anslist': coursesList
    },
    methods: {
        'getCourses': function(){
            uid = this.$route.params.id
            
            var main = this
            fetch('https://api.snsd0805.com/shared/'+uid)
                .then(function(response){
                    return response.json()
                }).then(function(jsonData){
                    main.selectCourses = JSON.parse(jsonData['data'])
                })
                .catch(function(err){
                    alert("錯誤： "+err)
                })                    
        }
    },
    template: `
    <div>
<!-- Navigation-->
<nav class="navbar navbar-expand-lg bg-secondary text-uppercase fixed-top" id="mainNav">
    <div class="container">
        <a class="navbar-brand js-scroll-trigger" href="#page-top">暨大排課表</a>
        <button class="navbar-toggler navbar-toggler-right text-uppercase font-weight-bold bg-primary text-white rounded" type="button" data-toggle="collapse" data-target="#navbarResponsive" aria-controls="navbarResponsive" aria-expanded="false" aria-label="Toggle navigation">
            Menu
            <i class="fas fa-bars"></i>
        </button>
        <div class="collapse navbar-collapse" id="navbarResponsive">
            <ul class="navbar-nav ml-auto">
                <li class="nav-item mx-0 mx-lg-1"><a class="nav-link py-3 px-0 px-lg-3 rounded js-scroll-trigger" href="https://github.com/snsd0805/NCNU_Course">Github</a></li>
            </ul>
        </div>
    </div>
</nav>
<br><br>


<section class="page-section portfolio" id="portfolio">
    <div class="container" id='table'>
        <!-- Portfolio Section Heading-->
        <h2 class="page-section-heading text-center text-uppercase text-secondary mb-0">跟你分享我的課表</h2>
        <!-- Icon Divider-->
        <div class="divider-custom">
            <div class="divider-custom-line"></div>
            <div class="divider-custom-icon"><i class="fas fa-star"></i></div>
            <div class="divider-custom-line"></div>
        </div>
        <div class="divider-custom">
            <div>
                <router-link to="/" class="btn btn-primary">安排我自己的課表</router-link>
            </div>
        </div>
        <div class="row">

            <div class="col-lg-12 table-responsive " >
                <course-table
                    v-bind:selectCourses="selectCourses"
                    v-bind:select_c="selectCourses"
                ></course-table>
            </div>
        </div>
        <!-- Portfolio Grid Items-->
    </div>
</section>


<div class="modal fade" id="myModal" tabindex="-1" role="dialog" aria-labelledby="exampleModalLabel" aria-hidden="true">
    <div class="modal-dialog">
        <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title" id="exampleModalLabel">資訊公告</h5>
                <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                    <span aria-hidden="true">×</span>
                </button>
            </div>
            <div class="modal-body">
                已經更新為 1092 新課表<br>
                但因學校未更新通識課資料，因此還沒有「通識課程分類」<br><br>
                2021 01/14 更新
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-secondary" data-dismiss="modal">我知道了</button>
            </div>
        </div>
    </div>
</div>
</div>
</div>
    `
}