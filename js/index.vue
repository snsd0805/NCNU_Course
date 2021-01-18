const Bar = { template: '<div>bar {{ $route.params.id }}</div>' }

Vue.use(VueRouter)
const router = new VueRouter({
    routes: [
        { path: '/', component: mainWindow },
        { path: '/share/:id', component: Bar }
    ]
})

var vm = new Vue({
    el: "#main",
    router
})