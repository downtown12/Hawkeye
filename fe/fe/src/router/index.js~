import Vue from 'vue'
import Router from 'vue-router'
import Setting from '@/components/Setting'
import Detail from '@/components/Detail'
import LeakageData from '@/components/LeakageData'
import ReportMenu from '@/components/ReportMenu'

Vue.use(Router);
const routes = [
  {path: '/', component: LeakageData},
  {path: '/view/tag/:tag', name:'tag',component: LeakageData},
  {path: '/view/leakage/:id', component: Detail},
  {path: '/setting', component: Setting},
  {path: '/reportmenu', component: ReportMenu},
];
export default new Router({
  routes
})
