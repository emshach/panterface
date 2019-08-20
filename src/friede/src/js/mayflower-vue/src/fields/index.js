export const BooleanField = () =>
   import(/* webpackChunkName: "fields" */ './BooleanField' )
export const CharField = () =>
   import(/* webpackChunkName: "fields" */ './CharField' )
export const TextField = () =>
   import(/* webpackChunkName: "fields" */ './TextField' )
export const JSONField = () =>
   import(/* webpackChunkName: "fields" */ './JSONField' )
export const ChoiceField = () =>
   import(/* webpackChunkName: "fields" */ './ChoiceField' )
export const TypedChoiceField = () =>
   import(/* webpackChunkName: "fields" */ './TypedChoiceField' )
export const DateField = () =>
   import(/* webpackChunkName: "fields" */ './DateField' )
export const DateTimeField = () =>
   import(/* webpackChunkName: "fields" */ './DateTimeField' )
export const DecimalField = () =>
   import(/* webpackChunkName: "fields" */ './DecimalField' )
export const DurationField = () =>
   import(/* webpackChunkName: "fields" */ './DurationField' )
export const EmailField = () =>
   import(/* webpackChunkName: "fields" */ './EmailField' )
export const FileField = () =>
   import(/* webpackChunkName: "fields" */ './FileField' )
export const FilePathField = () =>
   import(/* webpackChunkName: "fields" */ './FilePathField' )
export const FloatField = () =>
   import(/* webpackChunkName: "fields" */ './FloatField' )
export const ImageField = () =>
   import(/* webpackChunkName: "fields" */ './ImageField' )
export const IntegerField = () =>
   import(/* webpackChunkName: "fields" */ './IntegerField' )
export const IpAddressField = () =>
   import(/* webpackChunkName: "fields" */ './IPAddressField' )
export const MultipleChoiceField = () =>
   import(/* webpackChunkName: "fields" */ './MultipleChoiceField' )
export const GenericIpAddressField = () =>
   import(/* webpackChunkName: "fields" */ './GenericIPAddressField' )
export const TypedMultipleChoiceField = () =>
   import(/* webpackChunkName: "fields" */ './TypedMultipleChoiceField' )
export const NullBooleanField = () =>
   import(/* webpackChunkName: "fields" */ './NullBooleanField' )
export const RegexField = () =>
   import(/* webpackChunkName: "fields" */ './RegexField' )
export const SlugField = () =>
   import(/* webpackChunkName: "fields" */ './SlugField' )
export const TimeField = () =>
   import(/* webpackChunkName: "fields" */ './TimeField' )
export const UrlField = () =>
   import(/* webpackChunkName: "fields" */ './URLField' )
export const UuidField = () =>
   import(/* webpackChunkName: "fields" */ './UUIDField' )
export const ComboField = () =>
   import(/* webpackChunkName: "fields" */ './ComboField' )
export const MultiValueField = () =>
   import(/* webpackChunkName: "fields" */ './MultiValueField' )
export const SplitDateTimeField = () =>
   import(/* webpackChunkName: "fields" */ './SplitDateTimeField' )
export const ModelChoiceField = () =>
   import(/* webpackChunkName: "fields" */ './ModelChoiceField' )
export const ModelMultipleChoiceField = () =>
   import(/* webpackChunkName: "fields" */ './ModelMultipleChoiceField' )

export const ChoicesField = MultipleChoiceField;
export const TypedChoicesField = TypedMultipleChoiceField;
export const ModelField = ModelChoiceField;
export const ModelsField = ModelMultipleChoiceField;

export const fields = {
  BooleanField,
  CharField,
  TextField,
  JSONField,
  ChoiceField,
  TypedChoiceField,
  DateField,
  DateTimeField,
  DecimalField,
  DurationField,
  EmailField,
  FileField,
  FilePathField,
  FloatField,
  ImageField,
  IntegerField,
  IpAddressField,
  GenericIpAddressField,
  MultipleChoiceField,
  TypedMultipleChoiceField,
  NullBooleanField,
  RegexField,
  SlugField,
  TimeField,
  UrlField,
  UuidField,
  ComboField,
  MultiValueField,
  SplitDateTimeField,
  ModelChoiceField,
  ModelMultipleChoiceField,
  // shortcuts
  ChoicesField,
  TypedChoicesField,
  ModelField,
  ModelsField
}

export default fields
