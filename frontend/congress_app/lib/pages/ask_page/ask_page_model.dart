import '/backend/api_requests/api_calls.dart';
import '/flutter_flow/flutter_flow_util.dart';
import '/flutter_flow/form_field_controller.dart';
import '/pages/nave_barre/nave_barre_widget.dart';
import '/index.dart';
import 'ask_page_widget.dart' show AskPageWidget;
import 'package:flutter/material.dart';

class AskPageModel extends FlutterFlowModel<AskPageWidget> {
  ///  State fields for stateful widgets in this page.

  // State field(s) for questionField widget.
  FocusNode? questionFieldFocusNode;
  TextEditingController? questionFieldTextController;
  String? Function(BuildContext, String?)? questionFieldTextControllerValidator;
  // State field(s) for Orateur widget.
  int? orateurValue;
  FormFieldController<int>? orateurValueController;
  // State field(s) for anonCheck widget.
  bool? anonCheckValue;
  // Stores action output result for [Backend Call - API (CreateQuestionAnon)] action in sendBtn widget.
  ApiCallResponse? apiResultmio;
  // Stores action output result for [Backend Call - API (CreateQuestionIdentified)] action in sendBtn widget.
  ApiCallResponse? apiResult72q;
  // Model for NaveBarre component.
  late NaveBarreModel naveBarreModel;

  @override
  void initState(BuildContext context) {
    naveBarreModel = createModel(context, () => NaveBarreModel());
  }

  @override
  void dispose() {
    questionFieldFocusNode?.dispose();
    questionFieldTextController?.dispose();

    naveBarreModel.dispose();
  }
}
