import Vue from 'vue'
import VueRouter from 'vue-router'
import HomeView from '../views/HomeView.vue'
import DetectView from '@/views/DetectView.vue'
import AccountView from '@/views/AccountView.vue'
import LoginView from '@/views/LoginView.vue'
import RegisterView from '@/views/RegisterView.vue'
import ProfileView from '@/views/ProfileView.vue'
import HistoryView from '@/views/HistoryView.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/about',
    name: 'about',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/AboutView.vue')
  },
  {
    path: '/detect',
    name: 'detect',
    component: DetectView
  },
  {
    path: '/profile',
    name: 'profile',
    component: ProfileView
  },
  {
    path: '/history',
    name: 'history',
    component: HistoryView
  },
  {
    path: '/account',
    component: AccountView,
    children: [
      { path: '', redirect: '/account/login' },
      { path: 'login', component: LoginView },
      { path: 'register', component: RegisterView }
    ]
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

router.beforeEach((to, from, next) => {
  const isAuthenticated = !!localStorage.getItem('token')
  const authRequiredRoutes = ['/detect', '/history', '/profile']
  const authPages = ['/account/login', '/account/register', '/account']

  const requiresAuth = authRequiredRoutes.some(route => to.path.startsWith(route))
  const isAuthPage = authPages.includes(to.path)

  if (requiresAuth && !isAuthenticated) {
    next('/account/login')
  } else if (isAuthPage && isAuthenticated) {
    next('/profile')
  } else {
    next()
  }
})

export default router
