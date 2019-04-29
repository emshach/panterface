import extend from 'lodash/extend'
function inherit( child, base, props ) {
  child.prototype = _.create(base.prototype, extend({
    '_super': base.prototype,
    'constructor': child
  }, props));
  return child;
}
const objects = {}

 function Widget( obj, cls ) {
  if ( !cls )
    cls = Widget;
  if ( obj instanceof cls ) {
    return obj;
  }
  if ( this instanceof cls ) {
    this.init( obj );
    return this;
  }
  return new cls( obj );
}
inherit ( Widget, Object, {
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

function Model( obj, cls ) {
  if ( !cls )
    cls = Model;
  if ( obj instanceof cls ) {
    return obj;
  }
  if ( this instanceof cls ) {
    this.init( obj );
    return this;
  }
  return new cls( obj );
}
inherit( Model, Object, {
  init( obj ) {
  }
})

function Field( obj, cls ) {
  if ( !cls )
    cls = Field;
  if ( obj instanceof cls ) {
    return obj;
  }
  if ( this instanceof cls ) {
    this.init( obj );
    return this;
  }
  return new cls( obj );
}
inherit( Field, Object, {
  init( obj ) {
  }
})

export { objects, inherit, Widget, Model, Field }
