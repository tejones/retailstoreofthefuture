{{/*
Expand the name of the chart.
*/}}
{{- define "prediction.name" -}}
{{- .Values.predictionService.nameOverride | default "prediction" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "prediction.labels" -}}
helm.sh/chart: {{ include "global.chart" . }}
{{ include "prediction.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "prediction.selectorLabels" -}}
app.kubernetes.io/name: {{ include "prediction.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{/*
Create the name of the service account to use
*/}}
{{- define "prediction.serviceAccountName" -}}
{{- if .Values.predictionService.serviceAccount.create }}
{{- .Values.predictionService.serviceAccount.name | default (include "prediction.name" .) }}-serviceaccount
{{- else }}
{{- .Values.predictionService.serviceAccount.name | default "default" }}
{{- end }}
{{- end }}

{{- define "prediction.serviceName" -}}
{{- include "prediction.name" . }}-svc
{{- end }}

{{- define "prediction.servicePort" -}}
{{- .Values.predictionService.servicePort | default 80 -}}
{{- end }}
