{{/*
Expand the name of the chart.
*/}}
{{- define "recommendation.name" -}}
{{- .Values.recommendationService.nameOverride | default "recommendation" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "recommendation.labels" -}}
helm.sh/chart: {{ include "global.chart" . }}
{{ include "recommendation.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "recommendation.selectorLabels" -}}
app.kubernetes.io/name: {{ include "recommendation.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{/*
Create the name of the service account to use
*/}}
{{- define "recommendation.serviceAccountName" -}}
{{- if .Values.recommendationService.serviceAccount.create }}
{{- .Values.recommendationService.serviceAccount.name | default (include "recommendation.name" .) }}-serviceaccount
{{- else }}
{{- .Values.recommendationService.serviceAccount.name | default "default" }}
{{- end }}
{{- end }}

{{- define "recommendation.serviceName" -}}
{{- include "recommendation.name" . }}-svc
{{- end }}

{{- define "recommendation.servicePort" -}}
{{- .Values.recommendationService.servicePort | default 80 -}}
{{- end }}
