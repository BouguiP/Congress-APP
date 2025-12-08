import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';

class FFAppState extends ChangeNotifier {
  static FFAppState _instance = FFAppState._internal();

  factory FFAppState() {
    return _instance;
  }

  FFAppState._internal();

  static void reset() {
    _instance = FFAppState._internal();
  }

  Future initializePersistedState() async {
    prefs = await SharedPreferences.getInstance();
    _safeInit(() {
      _isFirstRun = prefs.getBool('ff_isFirstRun') ?? _isFirstRun;
    });
    _safeInit(() {
      _userRole = prefs.getString('ff_userRole') ?? _userRole;
    });
    _safeInit(() {
      _roleParticipantId =
          prefs.getInt('ff_roleParticipantId') ?? _roleParticipantId;
    });
    _safeInit(() {
      _participantId = prefs.getInt('ff_participantId') ?? _participantId;
    });
  }

  void update(VoidCallback callback) {
    callback();
    notifyListeners();
  }

  late SharedPreferences prefs;

  int _participantId = 0;
  int get participantId => _participantId;
  set participantId(int value) {
    _participantId = value;
    prefs.setInt('ff_participantId', value);
  }

  bool _sendAnonymously = false;
  bool get sendAnonymously => _sendAnonymously;
  set sendAnonymously(bool value) {
    _sendAnonymously = value;
  }

  bool _isFirstRun = true;
  bool get isFirstRun => _isFirstRun;
  set isFirstRun(bool value) {
    _isFirstRun = value;
    prefs.setBool('ff_isFirstRun', value);
  }

  String _userRole = '';
  String get userRole => _userRole;
  set userRole(String value) {
    _userRole = value;
    prefs.setString('ff_userRole', value);
  }

  int _roleParticipantId = 0;
  int get roleParticipantId => _roleParticipantId;
  set roleParticipantId(int value) {
    _roleParticipantId = value;
    prefs.setInt('ff_roleParticipantId', value);

  }

  String _selectedStatus = 'non_repondu';
  String get selectedStatus => _selectedStatus;
  set selectedStatus(String value) {
    _selectedStatus = value;
  }

  int _selectedSpeakerId = 0;
  int get selectedSpeakerId => _selectedSpeakerId;
  set selectedSpeakerId(int value) {
    _selectedSpeakerId = value;
  }
}

void _safeInit(Function() initializeField) {
  try {
    initializeField();
  } catch (_) {}
}

Future _safeInitAsync(Function() initializeField) async {
  try {
    await initializeField();
  } catch (_) {}
}
