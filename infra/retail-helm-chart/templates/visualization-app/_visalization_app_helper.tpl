{{/*
Expand the name of the chart.
*/}}
{{- define "visualization.name" -}}
{{- .Values.recommendationService.nameOverride | default "visualization" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "visualization.labels" -}}
helm.sh/chart: {{ include "global.chart" . }}
{{ include "visualization.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "visualization.selectorLabels" -}}
app.kubernetes.io/name: {{ include "visualization.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{/*
Create the name of the service account to use
*/}}
{{- define "visualization.serviceAccountName" -}}
{{- if .Values.visualization.serviceAccount.create }}
{{- .Values.visualization.serviceAccount.name | default (include "visualization.name" .) }}-serviceaccount
{{- else }}
{{- .Values.visualization.serviceAccount.name | default "default" }}
{{- end }}
{{- end }}

{{- define "visualization.serviceName" -}}
{{- include "visualization.name" . }}-svc
{{- end }}

{{- define "visualization.servicePort" -}}
{{- .Values.visualization.servicePort | default 80 -}}
{{- end }}
