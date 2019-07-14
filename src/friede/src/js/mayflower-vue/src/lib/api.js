import axios from 'axios'

export function process_args( args, data ) {
  var str_args = [ '/api' ];
  var obj_args = [{}];
  Array.prototype.forEach.call( args, f => {
    ( typeof f === 'string' ? str_args : obj_args ).push(f);
  });
  var out_args = [ str_args.join('/') ];
  if ( obj_args.length > 1 ) {
    if ( data ) {
      out_args.push( Object.assign.apply( null, obj_args ));
      out_args.push({
        xsrfCookieName: 'csrftoken',
        xsrfHeaderName: 'X-CSRFToken'
      });
    } else {
      out_args.push({
        xsrfCookieName: 'csrftoken',
        xsrfHeaderName: 'X-CSRFToken',
        params: Object.assign.apply( null, obj_args )
      });
    }
  }
  // TODO: make more sophisticated
  return out_args;
}

export function API() {
  return axios.get.apply( null, process_args( arguments ));
}

Object.assign( API, {
  // axios.request(config)
  request: axios.request,

  // axios.get(url[, config])
  get() {
    return axios.get.apply( null, process_args( arguments ));
  },

  // axios.post(url[, data[, config]])
  post() {
    return axios.post.apply( null, process_args( arguments, true ));
  },

  // axios.head(url[, config])
  header() {
    return axios.header.apply( null, process_args( arguments ));
  },

  // axios.options(url[, config])
  options() {
    return axios.options.apply( null, process_args( arguments ));
  },

  // axios.put(url[, data[, config]])
  put() {
    return axios.put.apply( null, process_args( arguments, true ));
  },

  // axios.patch(url[, data[, config]])
  patch() {
    return axios.patch.apply( null, process_args( arguments, true ));
  },

  // axios.delete(url[, config])
  delete() {
    return axios.delete.apply( null, process_args( arguments ));
  }
});

export default {
  API,
  install( Vue ) {
    Vue.$api = API;
    Vue.prototype.$api = API;
  }
}
