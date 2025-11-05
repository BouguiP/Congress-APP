import '/flutter_flow/flutter_flow_util.dart';
import '/pages/nave_barre/nave_barre_widget.dart';
import 'info_page_widget.dart' show InfoPageWidget;
import 'package:flutter/material.dart';

class InfoPageModel extends FlutterFlowModel<InfoPageWidget> {
  ///  State fields for stateful widgets in this page.

  // Model for NaveBarre component.
  late NaveBarreModel naveBarreModel;

  @override
  void initState(BuildContext context) {
    naveBarreModel = createModel(context, () => NaveBarreModel());
  }

  @override
  void dispose() {
    naveBarreModel.dispose();
  }
}
