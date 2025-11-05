import '/backend/api_requests/api_calls.dart';
import '/flutter_flow/flutter_flow_util.dart';
import '/pages/nave_barre/nave_barre_widget.dart';
import 'documents_widget.dart' show DocumentsWidget;
import 'package:flutter/material.dart';

class DocumentsModel extends FlutterFlowModel<DocumentsWidget> {
  ///  State fields for stateful widgets in this page.

  // Stores action output result for [Backend Call - API (ListDocuments)] action in Documents widget.
  ApiCallResponse? apiResulth5c;
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
