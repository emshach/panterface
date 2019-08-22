import create from 'lodash/create'
import extend from 'lodash/extend'
import isArray from 'lodash/isArray'
import isFunction from 'lodash/isFunction'
import { API } from '@/lib/api'
function inherit( child, base, props ) {
  child.prototype = create( base.prototype, extend({
    '_super': base.prototype,
    'constructor': child
  }, props ));
  return child;
}
const objects = {}

function Widget( obj, Cls ) {
  if ( !Cls )
    Cls = Widget;
  if ( obj instanceof Cls ) {
    return obj;
  }
  if ( this instanceof Cls ) {
    this.init( obj );
    return this;
  }
  return new Cls( obj || {} );
}
inherit( Widget, Object, {
  init( obj ) {
    if ( obj.extends ) {
      var e = obj.extends;
      var s = [ obj ];
      var d = {};
      var p = {
        icon: null,
        minX: null,
        minY: null,
        maxX: null,
        maxY: null,
        default: null,
        foramt: null,
      };
      while (e) {
        s.unshift(e);
        e = e.extends;
      }
      s.forEach(
        x => {
          Object.assign( d, x.data );
          if ( x.min_x )
            p.minX = x.min_x;
          if ( x.min_y )
            p.minY = x.min_y;
          if ( x.max_x )
            p.maxX = x.max_x;
          if ( x.max_y )
            p.maxY = x.max_y;
          if ( x.icon )
            p.icon = x.icon.name;
          if ( x.default )
            p.default = x.default;
          if (x.format )
            p.format = x.format;
        });
      p.data = d;
    }
    Object.assign( this, p );
  }
})

function EventObject( obj, Cls ) {
  if ( !Cls )
    Cls = Field;
  if ( obj instanceof Cls ) {
    return obj;
  }
  if ( this instanceof Cls ) {
    this.init( obj );
    return this;
  }
  return new Cls( obj || {} );
}
inherit( EventObject, Object, {
  init( obj ) {
    this.events = {};
    // TODO: super.init()
  },
  fire( event ) {
    // break out if handler returns false
    ( this.events[ event ] || [] ).find( f => f.apply( this, arguments ) === false );
  }
});

function Field( obj, Cls ) {
  if ( !Cls )
    Cls = Field;
  if ( obj instanceof Cls ) {
    return obj;
  }
  if ( this instanceof Cls ) {
    this.init( obj );
    return this;
  }
  return new Cls( obj || {} );
}
inherit( Field, EventObject, {
  init( obj ) {
    // TODO: super.init()
    this.meta = obj;
    this.events = {
      commit: [],
      revert: []
    };
    if ( this.meta.default && isArray( this.meta.default )
         && this.meta.default[0] === 'f')
      this.meta.default = eval( this.meta.default[1] );
    var val = this.meta.value || this.meta.default;
    this.value = isFunction( val ) ? val() : val;
    this.wip = this.value;
  },
  commit() {
    this.value = this.wip === undefined || this.wip === null ? '' : this.wip;
    this.fire( 'commit' );
  },
  revert() {
    this.wip = this.value;
  },
  oncommit(f) {
    this.events.commit.push(f);
    return this;
  }
})

function Model( obj, Cls ) {
  if ( !Cls )
    Cls = Model;
  if ( obj instanceof Cls ) {
    return obj;
  }
  if ( this instanceof Cls ) {
    this.init( obj );
    return this;
  }
  return new Cls( obj || {} );
}
inherit( Model, Object, {
  init( obj ) {
    this.meta = obj;
    this.data = {};
    this.changes = {};
    ( this.fields = obj.fields.map( x => Field(x).oncommit( field => {
      if ( field.value === undefined || field.value === '' )
        delete this.data[ field.name ];
      else
        this.data[ field.name ] = field.value;
      if ( !this.changes ) this.changes = { id: this.data.id }
      this.changes[ field.name ] = field.value;
      this.save( field.name, field.value );
    }))).forEach( field => {
      this.data[ field.name ] = field.value;
    });

    if ( this.data.id || !this.meta.rest )
      this.ready = new Promise(( s, j ) => s() );
    if ( !this.data.id && this.meta.rest ) {
      this.ready = API.post( this.meta.rest, '' ).then( r => {
        this.fields.forEach( field => {
          if ( field.meta.name in r.data )
            this.data[ field.meta.name ]
             = field.wip
             = field.value
             = r.data[ field.meta.name ];
        });
      }).catch( err => {
        console.log( 'error in model object init', err );
      });
    }
  },
  save( key, value ) {
    if ( !this.meta.rest ) return null;
    const changes = this.changes;
    this.changes = null;
    return API.post( this.meta.rest, key ? {[ key ]: value } : ( changes || this.data ))
       .catch( err => {
         console.log( 'error updating model object', err );
         this.changes = changes;
       });
  }
})

export { objects, inherit, Widget, Model, Field }
