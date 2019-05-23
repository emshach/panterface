import Vue from 'vue'
import Router from 'vue-router'
import store from './store'
import Home from './views/Home'

Vue.use( Router )

let user;

function getUser() {
  return Vue.prototype.$Amplify.Auth.currentAuthenticatedUser().then( data => {
    if ( data && data.signInUserSession ) {
      store.commit( 'setUser', data );
      return data;
    }
    return null;
  }).catch( e => {
    store.commit( 'setUser', null );
    return null
  });
}

const router = new Router({
  mode: 'history',
  base: '/',
  routes: [
    {
      path: '/',
      name: 'home',
      component: Home
    },
    // {
    //   path: '/about',
    //   name: 'about',
    //   // route level code-splitting
    //   // this generates a separate chunk (about.[hash].js) for this route
    //   // which is lazy-loaded when the route is visited.
    //   component: () => import(/* webpackChunkName: "about" */ './views/About')
    // }
  ]
});

router.beforeResolve( async ( to, from, next ) => {
  if ( to.matched.some( record => record.meta.requiresAuth )) {
    user = await getUser();
    if ( !user ) {
      return next({
        path: '/login',
        query: {
          redirect: to.fullPath,
        }
      });
    }
    if ( to != store.getters.getRoute ) {
      store.dispatch( 'setPath', to.fullPath );
    }
    return next()
  }
  if ( to != store.getters.getRoute ) {
    store.dispatch( 'setPath', to.fullPath );
  }
  return next()
});

export default router
