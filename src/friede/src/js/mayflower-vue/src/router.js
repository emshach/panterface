import Vue from 'vue'
import Router from 'vue-router'
import store from '@/store'
import Page from '@/views'

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
      path: '*',
      name: 'page',
      component: Page
    },
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
    if ( to.fullPath != store.getters.route ) {
      store.dispatch( 'setPath', to.fullPath );
    }
    return next()
  }
  if ( to.fullPath != store.getters.route ) {
    store.dispatch( 'setPath', to.fullPath );
  }
  return next()
});

export default router
