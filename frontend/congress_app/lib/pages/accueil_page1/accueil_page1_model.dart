import '/backend/api_requests/api_calls.dart';
import '/flutter_flow/flutter_flow_util.dart';
import '/pages/nave_barre/nave_barre_widget.dart';
import '/index.dart';
import 'accueil_page1_widget.dart' show AccueilPage1Widget;
import 'package:flutter/material.dart';

class AccueilPage1Model extends FlutterFlowModel<AccueilPage1Widget> {
  ///  Local state fields for this page.

  String? pCurrTitle;

  String? pCurrRoom;

  String? pCurrStart;

  String? pCurrEnd;

  String? pNextTitle;

  String? pNextStart;

  String? pNextEnd;

  String? pNextRoom;

  ///  State fields for stateful widgets in this page.

  // Stores action output result for [Backend Call - API (CurrentSessions)] action in AccueilPage1 widget.
  ApiCallResponse? apiResult5vf;
  // Stores action output result for [Backend Call - API (NextSession)] action in AccueilPage1 widget.
  ApiCallResponse? apiResultxl5;
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
