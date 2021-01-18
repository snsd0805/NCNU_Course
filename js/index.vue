Vue.use(VueRouter)
const router = new VueRouter({
    routes: [
        { path: '/', component: mainWindow },
        { path: '/share/:id', component: share }
    ]
})

var vm = new Vue({
    el: "#main",
    router
})