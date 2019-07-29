import axios from 'axios'
import isNumber from 'lodash/isNumber'
import isString from 'lodash/isString'

export function processArgs( args, data ) {
  var strArgs = [ '/api' ];
  var objArgs = [{}];
  Array.prototype.forEach.call( args, f => {
    ( isString(f) || isNumber(f) ? strArgs : objArgs ).push(f);
  });
  var outArgs = [ strArgs.join('/') ];
  if ( objArgs.length > 1 ) {
    if ( data ) {
      outArgs.push( Object.assign.apply( null, objArgs ));
      outArgs.push({
        xsrfCookieName: 'csrftoken',
        xsrfHeaderName: 'X-CSRFToken'
      });
    } else {
      outArgs.push({
        xsrfCookieName: 'csrftoken',
        xsrfHeaderName: 'X-CSRFToken',
        params: Object.assign.apply( null, objArgs )
      });
    }
  } else {
    outArgs.push({
      xsrfCookieName: 'csrftoken',
      xsrfHeaderName: 'X-CSRFToken'
    });
  }
  // TODO: make more sophisticated
  return outArgs;
}

export function API() {
  return axios.get.apply( null, processArgs( arguments ));
}

Object.assign( API, {
  // axios.request(config)
  request: axios.request,

  // axios.get(url[, config])
  get() {
    return axios.get.apply( null, processArgs( arguments ));
  },

  // axios.post(url[, data[, config]])
  post() {
    return axios.post.apply( null, processArgs( arguments, true ));
  },

  // axios.head(url[, config])
  header() {
    return axios.header.apply( null, processArgs( arguments ));
  },

  // axios.options(url[, config])
  options() {
    return axios.options.apply( null, processArgs( arguments ));
  },

  // axios.put(url[, data[, config]])
  put() {
    return axios.put.apply( null, processArgs( arguments, true ));
  },

  // axios.patch(url[, data[, config]])
  patch() {
    return axios.patch.apply( null, processArgs( arguments, true ));
  },

  // axios.delete(url[, config])
  delete() {
    return axios.delete.apply( null, processArgs( arguments ));
  }
});

export default {
  API,
  install( Vue ) {
    Vue.$api = API;
    Vue.prototype.$api = API;
  }
}
