export const JsonWidget = () => import(/* webpackChunkName: "json" */ './JsonWidget' );
export const JsonObject = () => import(/* webpackChunkName: "json" */ './JsonObject' );
export const JsonTuple = () => import(/* webpackChunkName: "json" */ './JsonTuple' );
export const JsonArray = () => import(/* webpackChunkName: "json" */ './JsonArray' );
export const JsonNumber = () => import(/* webpackChunkName: "json" */ './JsonNumber' );
export const JsonString = () => import(/* webpackChunkName: "json" */ './JsonString' );
export const JsonBoolean = () => import(/* webpackChunkName: "json" */ './JsonBoolean' );
export const JsonNull = () => import(/* webpackChunkName: "json" */ './JsonNull' );
export const JsonInvalid = () => import(/* webpackChunkName: "json" */ './JsonInvalid' );

export default {
  JsonWidget,
  JsonObject,
  JsonTuple,
  JsonArray,
  JsonNumber,
  JsonString,
  JsonBoolean,
  JsonNull,
  JsonInvalid,
}
