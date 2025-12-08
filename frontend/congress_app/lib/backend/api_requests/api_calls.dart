import 'dart:convert';
import 'package:flutter/foundation.dart';

import '/flutter_flow/flutter_flow_util.dart';
import 'api_manager.dart';

export 'api_manager.dart' show ApiCallResponse;

const _kPrivateApiFunctionName = 'ffPrivateApiCall';

class ListeSessionsCall {
  static Future<ApiCallResponse> call() async {
    return ApiManager.instance.makeApiCall(
      callName: 'Liste Sessions ',
      apiUrl:
          'https://congress-app-production.up.railway.app/sessions',
      callType: ApiCallType.GET,
      headers: {
        'Accept': 'application/json',
        'ngrok-skip-browser-warning': '1',
      },
      params: {},
      returnBody: true,
      encodeBodyUtf8: false,
      decodeUtf8: false,
      cache: false,
      isStreamingApi: false,
      alwaysAllowBody: false,
    );
  }
}

class CreateQuestionAnonCall {
  static Future<ApiCallResponse> call({
    int? defaultSessionId = 1,
    String? questionText = '',
    int? orateurId,
  }) async {
    final ffApiRequestBody = '''
{
  "session_id": ${defaultSessionId},
  "question_text": "${escapeStringForJson(questionText)}",
  "orateur_id": ${orateurId}
}''';
    return ApiManager.instance.makeApiCall(
      callName: 'CreateQuestionAnon',
      apiUrl:
          'https://congress-app-production.up.railway.app/questions',
      callType: ApiCallType.POST,
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'ngrok-skip-browser-warning': '1',
      },
      params: {},
      body: ffApiRequestBody,
      bodyType: BodyType.JSON,
      returnBody: true,
      encodeBodyUtf8: false,
      decodeUtf8: false,
      cache: false,
      isStreamingApi: false,
      alwaysAllowBody: false,
    );
  }
}

class ListOrateursForSessionCall {
  static Future<ApiCallResponse> call({
    int? sessionId = 1,
  }) async {
    return ApiManager.instance.makeApiCall(
      callName: 'ListOrateursForSession',
      apiUrl:
          'https://congress-app-production.up.railway.app/sessions/${sessionId}/orateurs',
      callType: ApiCallType.GET,
      headers: {
        'Accept': 'application/json',
        'ngrok-skip-browser-warning': '1',
        'Content-Type': 'application/json',
      },
      params: {},
      returnBody: true,
      encodeBodyUtf8: false,
      decodeUtf8: false,
      cache: false,
      isStreamingApi: false,
      alwaysAllowBody: false,
    );
  }

  static List<String>? nom(dynamic response) => (getJsonField(
        response,
        r'''$[:].nom''',
        true,
      ) as List?)
          ?.withoutNulls
          .map((x) => castToType<String>(x))
          .withoutNulls
          .toList();
  static List<int>? id(dynamic response) => (getJsonField(
        response,
        r'''$[:].id''',
        true,
      ) as List?)
          ?.withoutNulls
          .map((x) => castToType<int>(x))
          .withoutNulls
          .toList();
}

class RegisterParticipantCall {
  static Future<ApiCallResponse> call({
    String? nom = '',
    String? prenom = '',
    String? email = '',
    String? profession = '',
    int? roleId,
  }) async {
    final ffApiRequestBody = '''
{
  "nom": "${escapeStringForJson(nom)}",
  "prenom": "${escapeStringForJson(prenom)}",
  "email": "${escapeStringForJson(email)}",
  "profession": "${escapeStringForJson(profession)}",
  "role_id": ${roleId} 
}
''';
    return ApiManager.instance.makeApiCall(
      callName: 'RegisterParticipant',
      apiUrl:
          'https://congress-app-production.up.railway.app/participants/register',
      callType: ApiCallType.POST,
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'ngrok-skip-browser-warning': '1',
      },
      params: {},
      body: ffApiRequestBody,
      bodyType: BodyType.JSON,
      returnBody: true,
      encodeBodyUtf8: false,
      decodeUtf8: false,
      cache: false,
      isStreamingApi: false,
      alwaysAllowBody: false,
    );
  }

  static int? id(dynamic response) => castToType<int>(getJsonField(
        response,
        r'''$.id''',
      ));
}

class CreateQuestionIdentifiedCall {
  static Future<ApiCallResponse> call({
    int? defaultSessionId = 1,
    String? questionText = '',
    int? orateurId,
    int? participantId,
  }) async {
    final ffApiRequestBody = '''
{
  "session_id": ${defaultSessionId},
  "question_text": "${escapeStringForJson(questionText)}",
  "orateur_id": ${orateurId},
  "participant_id": ${participantId}
}''';
    return ApiManager.instance.makeApiCall(
      callName: 'CreateQuestionIdentified',
      apiUrl:
          'https://congress-app-production.up.railway.app/questions',
      callType: ApiCallType.POST,
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'ngrok-skip-browser-warning': '1',
      },
      params: {},
      body: ffApiRequestBody,
      bodyType: BodyType.JSON,
      returnBody: true,
      encodeBodyUtf8: false,
      decodeUtf8: false,
      cache: false,
      isStreamingApi: false,
      alwaysAllowBody: false,
    );
  }
}

class CurrentSessionsCall {
  static Future<ApiCallResponse> call() async {
    return ApiManager.instance.makeApiCall(
      callName: 'CurrentSessions',
      apiUrl:
          'https://congress-app-production.up.railway.app/sessions/current',
      callType: ApiCallType.GET,
      headers: {
        'Accept': 'application/json',
        'ngrok-skip-browser-warning': '1',
        'Content-Type': 'application/json',
      },
      params: {},
      returnBody: true,
      encodeBodyUtf8: false,
      decodeUtf8: false,
      cache: false,
      isStreamingApi: false,
      alwaysAllowBody: false,
    );
  }

  static int? id(dynamic response) => castToType<int>(getJsonField(
        response,
        r'''$[:].id''',
      ));
  static String? titre(dynamic response) => castToType<String>(getJsonField(
        response,
        r'''$[:].titre''',
      ));
  static List<String>? heuredebut(dynamic response) => (getJsonField(
        response,
        r'''$[:].heure_debut''',
        true,
      ) as List?)
          ?.withoutNulls
          .map((x) => castToType<String>(x))
          .withoutNulls
          .toList();
  static String? heurefin(dynamic response) => castToType<String>(getJsonField(
        response,
        r'''$[:].heure_fin''',
      ));
  static List<String>? conferenciers(dynamic response) => (getJsonField(
        response,
        r'''$[:].conferenciers''',
        true,
      ) as List?)
          ?.withoutNulls
          .map((x) => castToType<String>(x))
          .withoutNulls
          .toList();
  static String? salle(dynamic response) => castToType<String>(getJsonField(
        response,
        r'''$[:].salle''',
      ));
  static String? heuredebuthhmm(dynamic response) =>
      castToType<String>(getJsonField(
        response,
        r'''$[:].heure_debut_hhmm''',
      ));
  static String? heurefinhhmm(dynamic response) =>
      castToType<String>(getJsonField(
        response,
        r'''$[:].heure_fin_hhmm''',
      ));
}

class NextSessionCall {
  static Future<ApiCallResponse> call() async {
    return ApiManager.instance.makeApiCall(
      callName: 'NextSession',
      apiUrl:
          'https://congress-app-production.up.railway.app/sessions/next',
      callType: ApiCallType.GET,
      headers: {
        'Accept': 'application/json',
        'ngrok-skip-browser-warning': '1',
        'Content-Type': 'application/json',
      },
      params: {},
      returnBody: true,
      encodeBodyUtf8: false,
      decodeUtf8: false,
      cache: false,
      isStreamingApi: false,
      alwaysAllowBody: false,
    );
  }

  static int? id(dynamic response) => castToType<int>(getJsonField(
        response,
        r'''$.id''',
      ));
  static String? titre(dynamic response) => castToType<String>(getJsonField(
        response,
        r'''$.titre''',
      ));
  static String? heuredebut(dynamic response) =>
      castToType<String>(getJsonField(
        response,
        r'''$.heure_debut''',
      ));
  static String? heurefin(dynamic response) => castToType<String>(getJsonField(
        response,
        r'''$.heure_fin''',
      ));
  static List<String>? conferenciers(dynamic response) => (getJsonField(
        response,
        r'''$.conferenciers''',
        true,
      ) as List?)
          ?.withoutNulls
          .map((x) => castToType<String>(x))
          .withoutNulls
          .toList();
  static String? salle(dynamic response) => castToType<String>(getJsonField(
        response,
        r'''$.salle''',
      ));
  static String? heuredebuthhmm(dynamic response) =>
      castToType<String>(getJsonField(
        response,
        r'''$.heure_debut_hhmm''',
      ));
  static String? heurefinhhmm(dynamic response) =>
      castToType<String>(getJsonField(
        response,
        r'''$.heure_fin_hhmm''',
      ));
}

class ListDocumentsCall {
  static Future<ApiCallResponse> call() async {
    return ApiManager.instance.makeApiCall(
      callName: 'ListDocuments',
      apiUrl:
          'https://congress-app-production.up.railway.app/documents',
      callType: ApiCallType.GET,
      headers: {
        'Accept': 'application/json',
        'ngrok-skip-browser-warning': '1',
        'Content-Type': 'application/json',
      },
      params: {},
      returnBody: true,
      encodeBodyUtf8: false,
      decodeUtf8: false,
      cache: false,
      isStreamingApi: false,
      alwaysAllowBody: false,
    );
  }

  static List<String>? name(dynamic response) => (getJsonField(
        response,
        r'''$[:].name''',
        true,
      ) as List?)
          ?.withoutNulls
          .map((x) => castToType<String>(x))
          .withoutNulls
          .toList();
  static List<String>? url(dynamic response) => (getJsonField(
        response,
        r'''$[:].url''',
        true,
      ) as List?)
          ?.withoutNulls
          .map((x) => castToType<String>(x))
          .withoutNulls
          .toList();
  static List<String>? type(dynamic response) => (getJsonField(
        response,
        r'''$[:].type''',
        true,
      ) as List?)
          ?.withoutNulls
          .map((x) => castToType<String>(x))
          .withoutNulls
          .toList();
  static List<String>? sizelabel(dynamic response) => (getJsonField(
        response,
        r'''$[:].size_label''',
        true,
      ) as List?)
          ?.withoutNulls
          .map((x) => castToType<String>(x))
          .withoutNulls
          .toList();
}

class LoginModerateurCall {
  static Future<ApiCallResponse> call({
    String? email = '',
    String? password = '',
  }) async {
    final ffApiRequestBody = '''
{
  "email": "${escapeStringForJson(email)}",
  "password": "${escapeStringForJson(password)}"
}''';
    return ApiManager.instance.makeApiCall(
      callName: 'LoginModerateur',
      apiUrl:
          'https://congress-app-production.up.railway.app/login',
      callType: ApiCallType.POST,
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'ngrok-skip-browser-warning': '1',
      },
      params: {},
      body: ffApiRequestBody,
      bodyType: BodyType.JSON,
      returnBody: true,
      encodeBodyUtf8: false,
      decodeUtf8: false,
      cache: false,
      isStreamingApi: false,
      alwaysAllowBody: false,
    );
  }

  static String? role(dynamic response) => castToType<String>(getJsonField(
        response,
        r'''$.role''',
      ));
}

class ListQuestionsModerNonReponduCall {
  static Future<ApiCallResponse> call({
    int? sessionId = 1,
    String? status = 'non_repondu',
    int? orateurId = 1,
  }) async {
    return ApiManager.instance.makeApiCall(
      callName: 'ListQuestionsModerNonRepondu',
      apiUrl:
          'https://congress-app-production.up.railway.app/questions',
      callType: ApiCallType.GET,
      headers: {
        'Accept': 'application/json',
        'ngrok-skip-browser-warning': '1',
        'Content-Type': 'application/json',
      },
      params: {
        'session_id': sessionId,
        'status': status,
        'orateur_id': orateurId,
      },
      returnBody: true,
      encodeBodyUtf8: false,
      decodeUtf8: false,
      cache: false,
      isStreamingApi: false,
      alwaysAllowBody: false,
    );
  }

  static int? id(dynamic response) => castToType<int>(getJsonField(
        response,
        r'''$[:].id''',
      ));
  static String? questiontext(dynamic response) =>
      castToType<String>(getJsonField(
        response,
        r'''$[:].question_text''',
      ));
  static String? createdat(dynamic response) => castToType<String>(getJsonField(
        response,
        r'''$[:].created_at''',
      ));
  static String? status(dynamic response) => castToType<String>(getJsonField(
        response,
        r'''$[:].status''',
      ));
  static String? session(dynamic response) => castToType<String>(getJsonField(
        response,
        r'''$[:].session''',
      ));
  static String? participant(dynamic response) =>
      castToType<String>(getJsonField(
        response,
        r'''$[:].participant''',
      ));
  static String? orateur(dynamic response) => castToType<String>(getJsonField(
        response,
        r'''$[:].orateur''',
      ));
}

class ToggleQuestionStatusCall {
  static Future<ApiCallResponse> call({
    int? questionId,
  }) async {
    return ApiManager.instance.makeApiCall(
      callName: 'ToggleQuestionStatus',
      apiUrl:
          'https://congress-app-production.up.railway.app/questions/${questionId}/toggle',
      callType: ApiCallType.PATCH,
      headers: {
        'Accept': 'application/json',
        'ngrok-skip-browser-warning': '1',
      },
      params: {},
      bodyType: BodyType.JSON,
      returnBody: true,
      encodeBodyUtf8: false,
      decodeUtf8: false,
      cache: false,
      isStreamingApi: false,
      alwaysAllowBody: false,
    );
  }

  static int? id(dynamic response) => castToType<int>(getJsonField(
        response,
        r'''$.id''',
      ));
  static String? questiontext(dynamic response) =>
      castToType<String>(getJsonField(
        response,
        r'''$.question_text''',
      ));
  static String? createdat(dynamic response) => castToType<String>(getJsonField(
        response,
        r'''$.created_at''',
      ));
  static String? status(dynamic response) => castToType<String>(getJsonField(
        response,
        r'''$.status''',
      ));
  static String? session(dynamic response) => castToType<String>(getJsonField(
        response,
        r'''$.session''',
      ));
  static String? participant(dynamic response) =>
      castToType<String>(getJsonField(
        response,
        r'''$.participant''',
      ));
  static String? orateur(dynamic response) => castToType<String>(getJsonField(
        response,
        r'''$.orateur''',
      ));
}

class ListQuestionsModerReponduCall {
  static Future<ApiCallResponse> call({
    int? sessionId = 1,
    String? status = 'repondu',
    int? orateurId = 1,
  }) async {
    return ApiManager.instance.makeApiCall(
      callName: 'ListQuestionsModerRepondu',
      apiUrl:
          'https://congress-app-production.up.railway.app/questions',
      callType: ApiCallType.GET,
      headers: {
        'Accept': 'application/json',
        'ngrok-skip-browser-warning': '1',
        'Content-Type': 'application/json',
      },
      params: {
        'session_id': sessionId,
        'status': status,
        'orateur_id': orateurId,
      },
      returnBody: true,
      encodeBodyUtf8: false,
      decodeUtf8: false,
      cache: false,
      isStreamingApi: false,
      alwaysAllowBody: false,
    );
  }

  static int? id(dynamic response) => castToType<int>(getJsonField(
        response,
        r'''$[:].id''',
      ));
  static String? questiontext(dynamic response) =>
      castToType<String>(getJsonField(
        response,
        r'''$[:].question_text''',
      ));
  static String? createdat(dynamic response) => castToType<String>(getJsonField(
        response,
        r'''$[:].created_at''',
      ));
  static String? status(dynamic response) => castToType<String>(getJsonField(
        response,
        r'''$[:].status''',
      ));
  static String? session(dynamic response) => castToType<String>(getJsonField(
        response,
        r'''$[:].session''',
      ));
  static dynamic participant(dynamic response) => getJsonField(
        response,
        r'''$[:].participant''',
      );
  static String? orateur(dynamic response) => castToType<String>(getJsonField(
        response,
        r'''$[:].orateur''',
      ));
}

class ApiPagingParams {
  int nextPageNumber = 0;
  int numItems = 0;
  dynamic lastResponse;

  ApiPagingParams({
    required this.nextPageNumber,
    required this.numItems,
    required this.lastResponse,
  });

  @override
  String toString() =>
      'PagingParams(nextPageNumber: $nextPageNumber, numItems: $numItems, lastResponse: $lastResponse,)';
}

String _toEncodable(dynamic item) {
  return item;
}

String _serializeList(List? list) {
  list ??= <String>[];
  try {
    return json.encode(list, toEncodable: _toEncodable);
  } catch (_) {
    if (kDebugMode) {
      print("List serialization failed. Returning empty list.");
    }
    return '[]';
  }
}

String _serializeJson(dynamic jsonVar, [bool isList = false]) {
  jsonVar ??= (isList ? [] : {});
  try {
    return json.encode(jsonVar, toEncodable: _toEncodable);
  } catch (_) {
    if (kDebugMode) {
      print("Json serialization failed. Returning empty json.");
    }
    return isList ? '[]' : '{}';
  }
}

String? escapeStringForJson(String? input) {
  if (input == null) {
    return null;
  }
  return input
      .replaceAll('\\', '\\\\')
      .replaceAll('"', '\\"')
      .replaceAll('\n', '\\n')
      .replaceAll('\t', '\\t');
}
