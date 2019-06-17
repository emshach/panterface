export const BaseWidget = () =>
   import(/* webpackChunkName: "widgets" */ './BaseWidget' )
export const CardWidget = () =>
   import(/* webpackChunkName: "widgets" */ './CardWidget' )
export const DashboardWidget = () =>
   import(/* webpackChunkName: "widgets" */ './DashboardWidget' )
export const InlineWidget = () =>
   import(/* webpackChunkName: "widgets" */ './InlineWidget' )
export const AdaptiveWidget = () =>
   import(/* webpackChunkName: "widgets" */ './AdaptiveWidget' )
export const ViewModelWidget = () =>
   import(/* webpackChunkName: "widgets" */ './ViewModelWidget' )
export const ActionHelpWidget = () =>
   import(/* webpackChunkName: "widgets" */ './ActionHelpWidget' )
export const DefaultActionWidget = () =>
   import(/* webpackChunkName: "widgets" */ './DefaultActionWidget' )
export const EditModelWidget = () =>
   import(/* webpackChunkName: "widgets" */ './EditModelWidget' )
export const ModelFieldWidget = () =>
   import(/* webpackChunkName: "widgets" */ './ModelFieldWidget' )
export const NewModelWidget = () =>
   import(/* webpackChunkName: "widgets" */ './NewModelWidget' )
export const ReportModelWidget = () =>
   import(/* webpackChunkName: "widgets" */ './ReportModelWidget' )

// export const ListModelWidget = () =>
//         import(/* webpackChunkName: "widgets" */ './ListModelWidget' )
// export const NewModelWidget = () =>
//         import(/* webpackChunkName: "widgets" */ './NewModelWidget' )
// export const EditModelWidget = () =>
//         import(/* webpackChunkName: "widgets" */ './EditModelWidget' )
// export const ReportModelWidget = () =>
//         import(/* webpackChunkName: "widgets" */ './ReportModelWidget' )
// export const ModelWidget = () =>
//         import(/* webpackChunkName: "widgets" */ './ModelWidget' )
// export const AddModelWidget = () =>
//         import/* webpackChunkName: "widgets" */( './AddModelWidget' )
// export const RemoveModelWidget = () =>
//         import/* webpackChunkName: "widgets" */( './RemoveModelWidget' )

export const widgets = {
  BaseWidget,
  CardWidget,
  DashboardWidget,
  InlineWidget,
  AdaptiveWidget,
  ViewModelWidget,
  ActionHelpWidget,
  DefaultActionWidget,
  EditModelWidget,
  ModelFieldWidget,
  NewModelWidget,
  ReportModelWidget,
  // ListModelWidget,
  // NewModelWidget,
  // EditModelWidget,
  // ReportModelWidget,
  // ModelWidget,
  // AddModelWidget,
  // RemoveModelWidget,
}

export default widgets

