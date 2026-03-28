#!/usr/bin/env bash
# Render all 13 Manim animations.
# Usage:  bash render_all.sh [quality]
#   quality: l = 480p15  |  m = 720p30 (default)  |  h = 1080p60  |  k = 2160p60
#
# Each video is saved under <folder>/media/videos/scene/<quality>/

set -e
QUALITY=${1:-m}
BASE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

declare -A SCENES=(
  [01_image_vs_graph]=ImageVsGraph
  [02_message_passing]=MessagePassing
  [03_cnn_vs_gcn]=CNNvsGCN
  [04_decision_tree]=DecisionTree
  [05_random_forest]=RandomForest
  [06_adjacency_matrix]=AdjacencyMatrix
  [07_laplacian_quadratic]=LaplacianQuadratic
  [08_spectral_clustering]=SpectralClustering
  [09_cheeger_inequality]=CheegerInequality
  [10_random_walk]=RandomWalk
  [11_receptive_field]=ReceptiveField
  [12_embedding_propagation]=EmbeddingPropagation
  [13_over_smoothing_squashing]=OverSmoothingSquashing
)

# Preserve order
FOLDERS=(
  01_image_vs_graph
  02_message_passing
  03_cnn_vs_gcn
  04_decision_tree
  05_random_forest
  06_adjacency_matrix
  07_laplacian_quadratic
  08_spectral_clustering
  09_cheeger_inequality
  10_random_walk
  11_receptive_field
  12_embedding_propagation
  13_over_smoothing_squashing
)

echo "Quality flag: -q${QUALITY}"
echo ""

for folder in "${FOLDERS[@]}"; do
  scene="${SCENES[$folder]}"
  echo "══════════════════════════════════════════"
  echo "  Rendering: $scene"
  echo "══════════════════════════════════════════"
  cd "$BASE/$folder"
  manim -q"${QUALITY}" --disable_caching --format=mp4 scene.py "$scene"
  find "$BASE/$folder/media/videos/scene" -type d -name partial_movie_files -prune -exec rm -rf {} +
  cd "$BASE"
  echo ""
done

echo "✓  All animations rendered."
echo ""
echo "Videos are in each folder under media/videos/scene/"
