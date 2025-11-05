import '/backend/api_requests/api_calls.dart';
import '/flutter_flow/flutter_flow_util.dart';
import '/flutter_flow/form_field_controller.dart';
import '/pages/nave_barre/nave_barre_widget.dart';
import 'dart:async';
import 'questio_manager_widget.dart' show QuestioManagerWidget;
import 'package:flutter/material.dart';

class QuestioManagerModel extends FlutterFlowModel<QuestioManagerWidget> {
  ///  State fields for stateful widgets in this page.

  // State field(s) for TabBar widget.
  TabController? tabBarController;
  int get tabBarCurrentIndex =>
      tabBarController != null ? tabBarController!.index : 0;
  int get tabBarPreviousIndex =>
      tabBarController != null ? tabBarController!.previousIndex : 0;

  // State field(s) for DropDown widget.
  int? dropDownValue1;
  FormFieldController<int>? dropDownValueController1;
  Completer<ApiCallResponse>? apiRequestCompleter1;
  // State field(s) for Checkbox widget.
  Map<dynamic, bool> checkboxValueMap1 = {};
  List<dynamic> get checkboxCheckedItems1 => checkboxValueMap1.entries
      .where((e) => e.value)
      .map((e) => e.key)
      .toList();

  // Stores action output result for [Backend Call - API (ToggleQuestionStatus)] action in Checkbox widget.
  ApiCallResponse? apiResult5zj;
  // Stores action output result for [Backend Call - API (ToggleQuestionStatus)] action in Checkbox widget.
  ApiCallResponse? apiResultgno;
  // State field(s) for Checkbox widget.
  Map<dynamic, bool> checkboxValueMap2 = {};
  List<dynamic> get checkboxCheckedItems2 => checkboxValueMap2.entries
      .where((e) => e.value)
      .map((e) => e.key)
      .toList();

  // State field(s) for Checkbox widget.
  Map<dynamic, bool> checkboxValueMap3 = {};
  List<dynamic> get checkboxCheckedItems3 => checkboxValueMap3.entries
      .where((e) => e.value)
      .map((e) => e.key)
      .toList();

  // State field(s) for Checkbox widget.
  Map<dynamic, bool> checkboxValueMap4 = {};
  List<dynamic> get checkboxCheckedItems4 => checkboxValueMap4.entries
      .where((e) => e.value)
      .map((e) => e.key)
      .toList();

  // State field(s) for DropDown widget.
  int? dropDownValue2;
  FormFieldController<int>? dropDownValueController2;
  Completer<ApiCallResponse>? apiRequestCompleter2;
  // State field(s) for Checkbox widget.
  Map<dynamic, bool> checkboxValueMap5 = {};
  List<dynamic> get checkboxCheckedItems5 => checkboxValueMap5.entries
      .where((e) => e.value)
      .map((e) => e.key)
      .toList();

  // Stores action output result for [Backend Call - API (ToggleQuestionStatus)] action in Checkbox widget.
  ApiCallResponse? apiResults62;
  // Stores action output result for [Backend Call - API (ToggleQuestionStatus)] action in Checkbox widget.
  ApiCallResponse? apiResultltq;
  // State field(s) for Checkbox widget.
  Map<dynamic, bool> checkboxValueMap6 = {};
  List<dynamic> get checkboxCheckedItems6 => checkboxValueMap6.entries
      .where((e) => e.value)
      .map((e) => e.key)
      .toList();

  // State field(s) for Checkbox widget.
  Map<dynamic, bool> checkboxValueMap7 = {};
  List<dynamic> get checkboxCheckedItems7 => checkboxValueMap7.entries
      .where((e) => e.value)
      .map((e) => e.key)
      .toList();

  // State field(s) for Checkbox widget.
  Map<dynamic, bool> checkboxValueMap8 = {};
  List<dynamic> get checkboxCheckedItems8 => checkboxValueMap8.entries
      .where((e) => e.value)
      .map((e) => e.key)
      .toList();

  // Model for NaveBarre component.
  late NaveBarreModel naveBarreModel;

  @override
  void initState(BuildContext context) {
    naveBarreModel = createModel(context, () => NaveBarreModel());
  }

  @override
  void dispose() {
    tabBarController?.dispose();
    naveBarreModel.dispose();
  }

  /// Additional helper methods.
  Future waitForApiRequestCompleted1({
    double minWait = 0,
    double maxWait = double.infinity,
  }) async {
    final stopwatch = Stopwatch()..start();
    while (true) {
      await Future.delayed(Duration(milliseconds: 50));
      final timeElapsed = stopwatch.elapsedMilliseconds;
      final requestComplete = apiRequestCompleter1?.isCompleted ?? false;
      if (timeElapsed > maxWait || (requestComplete && timeElapsed > minWait)) {
        break;
      }
    }
  }

  Future waitForApiRequestCompleted2({
    double minWait = 0,
    double maxWait = double.infinity,
  }) async {
    final stopwatch = Stopwatch()..start();
    while (true) {
      await Future.delayed(Duration(milliseconds: 50));
      final timeElapsed = stopwatch.elapsedMilliseconds;
      final requestComplete = apiRequestCompleter2?.isCompleted ?? false;
      if (timeElapsed > maxWait || (requestComplete && timeElapsed > minWait)) {
        break;
      }
    }
  }
}
