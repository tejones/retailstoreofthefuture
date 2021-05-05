{{/*
Expand the name of the chart.
*/}}
{{- define "bridge.name" -}}
{{- .Values.predictionService.nameOverride | default "bridge" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "bridge.labels" -}}
helm.sh/chart: {{ include "global.chart" . }}
{{ include "bridge.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "bridge.selectorLabels" -}}
app.kubernetes.io/name: {{ include "bridge.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{/*
Create the name of the service account to use
*/}}
{{- define "bridge.serviceAccountName" -}}
{{- if .Values.predictionService.serviceAccount.create }}
{{- .Values.predictionService.serviceAccount.name | default (include "bridge.name" .) }}-serviceaccount
{{- else }}
{{- .Values.predictionService.serviceAccount.name | default "default" }}
{{- end }}
{{- end }}