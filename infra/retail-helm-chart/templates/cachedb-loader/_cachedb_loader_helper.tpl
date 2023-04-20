{{/*
Expand the name of the chart.
*/}}
{{- define "cachedbLoader.name" -}}
{{- .Values.cachedbLoader.nameOverride | default "cachedb-loader" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "cachedbLoader.labels" -}}
helm.sh/chart: {{ include "global.chart" . }}
{{ include "cachedbLoader.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "cachedbLoader.selectorLabels" -}}
app.kubernetes.io/name: {{ include "cachedbLoader.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{/*
Create the name of the service account to use
*/}}
{{- define "cachedbLoader.serviceAccountName" -}}
{{- if .Values.cachedbLoader.serviceAccount.create }}
{{- .Values.cachedbLoader.serviceAccount.name | default (include "cachedbLoader.name" .) }}-serviceaccount
{{- else }}
{{- .Values.cachedbLoader.serviceAccount.name | default "default" }}
{{- end }}
{{- end }}
