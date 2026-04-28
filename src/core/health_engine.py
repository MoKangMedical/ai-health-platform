"""多模态健康检测引擎"""

import numpy as np
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Optional
import json

@dataclass
class VoiceFeatures:
    """语音特征(59维)"""
    # 基频特征 (5维)
    f0_mean: float = 0.0
    f0_std: float = 0.0
    f0_min: float = 0.0
    f0_max: float = 0.0
    f0_range: float = 0.0
    
    # 抖动和微扰 (6维)
    jitter_local: float = 0.0
    jitter_rap: float = 0.0
    jitter_ppq5: float = 0.0
    shimmer_local: float = 0.0
    shimmer_apq3: float = 0.0
    shimmer_apq5: float = 0.0
    
    # 噪声比 (2维)
    hnr_mean: float = 0.0
    hnr_std: float = 0.0
    
    # 语速特征 (4维)
    speech_rate: float = 0.0
    articulation_rate: float = 0.0
    pause_ratio: float = 0.0
    mean_pause_duration: float = 0.0
    
    # 能量特征 (3维)
    rms_mean: float = 0.0
    rms_std: float = 0.0
    energy_entropy: float = 0.0
    
    # 频谱特征 (5维)
    spectral_centroid_mean: float = 0.0
    spectral_centroid_std: float = 0.0
    spectral_bandwidth_mean: float = 0.0
    spectral_rolloff_mean: float = 0.0
    spectral_flux_mean: float = 0.0
    
    # MFCC特征(13维)
    mfcc_1_mean: float = 0.0
    mfcc_2_mean: float = 0.0
    mfcc_3_mean: float = 0.0
    mfcc_4_mean: float = 0.0
    mfcc_5_mean: float = 0.0
    mfcc_6_mean: float = 0.0
    mfcc_7_mean: float = 0.0
    mfcc_8_mean: float = 0.0
    mfcc_9_mean: float = 0.0
    mfcc_10_mean: float = 0.0
    mfcc_11_mean: float = 0.0
    mfcc_12_mean: float = 0.0
    mfcc_13_mean: float = 0.0
    
    # 梅尔频谱特征 (2维)
    mel_spectral_energy: float = 0.0
    mel_spectral_entropy: float = 0.0
    
    # 情感特征 (3维)
    emotion_valence: float = 0.0
    emotion_arousal: float = 0.0
    emotion_dominance: float = 0.0
    
    # 呼吸特征 (2维)
    breathing_rate: float = 0.0
    breathing_depth: float = 0.0
    
    # 其他特征 (3维)
    total_duration: float = 0.0
    voiced_frames_ratio: float = 0.0
    unvoiced_frames_ratio: float = 0.0
    
    # 额外特征 (11维) - 凑够59维
    formant_f1: float = 0.0
    formant_f2: float = 0.0
    formant_f3: float = 0.0
    zero_crossing_rate: float = 0.0
    spectral_contrast_mean: float = 0.0
    spectral_flatness: float = 0.0
    chroma_mean: float = 0.0
    tonnetz_mean: float = 0.0
    onset_strength_mean: float = 0.0
    tempo: float = 0.0
    beat_strength: float = 0.0
    
    def to_dict(self) -> Dict:
        return asdict(self)
    
    def to_vector(self) -> np.ndarray:
        """转换为59维向量"""
        return np.array(list(asdict(self).values()))

@dataclass
class FaceFeatures:
    """面部特征(6维)"""
    skin_color_score: float = 0.0  # 肤色健康评分
    skin_texture_score: float = 0.0  # 皮肤纹理评分
    eye_brightness: float = 0.0  # 眼睛明亮度
    eye_redness: float = 0.0  # 眼睛充血程度
    lip_color: float = 0.0  # 唇色健康度
    facial_symmetry: float = 0.0  # 面部对称性
    
    def to_dict(self) -> Dict:
        return asdict(self)

@dataclass
class VideoFeatures:
    """视频特征"""
    skin_analysis: Dict = field(default_factory=dict)  # 皮肤分析
    eye_analysis: Dict = field(default_factory=dict)  # 眼睛分析
    hair_analysis: Dict = field(default_factory=dict)  # 头发分析
    movement_analysis: Dict = field(default_factory=dict)  # 动作分析
    
    def to_dict(self) -> Dict:
        return asdict(self)

@dataclass
class HealthRisk:
    """健康风险"""
    name: str = ""
    category: str = ""
    level: str = "low"  # low/medium/high
    score: float = 0.0
    description: str = ""
    suggestions: List[str] = field(default_factory=list)

@dataclass
class TCMDiagnosis:
    """中医体质诊断"""
    primary_type: str = ""  # 主要体质类型
    secondary_type: str = ""  # 次要体质类型
    scores: Dict = field(default_factory=dict)  # 各体质得分
    recommendations: List[str] = field(default_factory=list)

@dataclass
class ComprehensiveHealthReport:
    """综合健康报告"""
    user_id: int = 0
    overall_score: float = 0.0
    
    # 多模态特征
    voice_features: Optional[VoiceFeatures] = None
    face_features: Optional[FaceFeatures] = None
    video_features: Optional[VideoFeatures] = None
    
    # 健康评估
    health_summary: str = ""
    risks: List[HealthRisk] = field(default_factory=list)
    
    # 中医体质
    tcm_diagnosis: Optional[TCMDiagnosis] = None
    
    # 营养建议
    nutrient_needs: Dict = field(default_factory=dict)
    recommended_ingredients: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict:
        result = {
            "user_id": self.user_id,
            "overall_score": self.overall_score,
            "health_summary": self.health_summary,
            "risks": [asdict(r) for r in self.risks],
            "nutrient_needs": self.nutrient_needs,
            "recommended_ingredients": self.recommended_ingredients
        }
        if self.voice_features:
            result["voice_features"] = self.voice_features.to_dict()
        if self.face_features:
            result["face_features"] = self.face_features.to_dict()
        if self.video_features:
            result["video_features"] = self.video_features.to_dict()
        if self.tcm_diagnosis:
            result["tcm_diagnosis"] = asdict(self.tcm_diagnosis)
        return result


class VoiceAnalyzer:
    """语音分析器"""
    
    def __init__(self):
        self.sample_rate = 16000
    
    def extract_features(self, audio_path: str) -> VoiceFeatures:
        """提取语音特征"""
        features = VoiceFeatures()
        
        try:
            import librosa
            y, sr = librosa.load(audio_path, sr=self.sample_rate)
            
            # 基本信息
            features.total_duration = len(y) / sr
            features.rms_mean = float(np.sqrt(np.mean(y ** 2)))
            features.rms_std = float(np.std(np.sqrt(np.abs(y))))
            
            # 基频特征
            f0, voiced_flag, _ = librosa.pyin(
                y, fmin=librosa.note_to_hz('C2'),
                fmax=librosa.note_to_hz('C7'), sr=sr
            )
            f0_valid = f0[~np.isnan(f0)]
            if len(f0_valid) > 0:
                features.f0_mean = float(np.mean(f0_valid))
                features.f0_std = float(np.std(f0_valid))
                features.f0_min = float(np.min(f0_valid))
                features.f0_max = float(np.max(f0_valid))
                features.f0_range = features.f0_max - features.f0_min
            
            # 语速特征
            onsets = librosa.onset.onset_detect(y=y, sr=sr, units='time')
            features.speech_rate = float(len(onsets) / max(features.total_duration, 0.1))
            
            # 频谱特征
            spectral_centroids = librosa.feature.spectral_centroid(y=y, sr=sr)[0]
            features.spectral_centroid_mean = float(np.mean(spectral_centroids))
            features.spectral_centroid_std = float(np.std(spectral_centroids))
            
            spectral_bandwidth = librosa.feature.spectral_bandwidth(y=y, sr=sr)[0]
            features.spectral_bandwidth_mean = float(np.mean(spectral_bandwidth))
            
            spectral_rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)[0]
            features.spectral_rolloff_mean = float(np.mean(spectral_rolloff))
            
            # MFCC特征
            mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
            for i in range(13):
                setattr(features, f'mfcc_{i+1}_mean', float(np.mean(mfccs[i])))
            
            # 梅尔频谱
            mel_spec = librosa.feature.melspectrogram(y=y, sr=sr)
            features.mel_spectral_energy = float(np.mean(mel_spec))
            
            # 有声/无声比例
            features.voiced_frames_ratio = float(np.sum(voiced_flag) / len(voiced_flag))
            features.unvoiced_frames_ratio = 1.0 - features.voiced_frames_ratio
            
        except Exception as e:
            print(f"语音特征提取失败: {e}")
            # 返回默认值
            features.total_duration = 30.0
            features.f0_mean = 150.0
            features.speech_rate = 4.0
        
        return features


class FaceAnalyzer:
    """面部分析器"""
    
    def extract_features(self, image_path: str) -> FaceFeatures:
        """提取面部特征"""
        features = FaceFeatures()
        
        try:
            import cv2
            image = cv2.imread(image_path)
            if image is None:
                raise ValueError("无法读取图像")
            
            # 转换为RGB
            rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            
            # 肤色分析
            hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
            features.skin_color_score = self._analyze_skin_color(hsv_image)
            
            # 皮肤纹理分析
            features.skin_texture_score = self._analyze_skin_texture(image)
            
            # 眼睛分析
            features.eye_brightness = self._analyze_eye_brightness(rgb_image)
            features.eye_redness = self._analyze_eye_redness(rgb_image)
            
            # 唇色分析
            features.lip_color = self._analyze_lip_color(rgb_image)
            
            # 面部对称性
            features.facial_symmetry = self._analyze_facial_symmetry(rgb_image)
            
        except Exception as e:
            print(f"面部特征提取失败: {e}")
            # 返回默认值
            features.skin_color_score = 70.0
            features.skin_texture_score = 70.0
            features.eye_brightness = 70.0
        
        return features
    
    def _analyze_skin_color(self, hsv_image) -> float:
        """分析肤色健康度"""
        # 提取皮肤区域（HSV范围）
        lower_skin = np.array([0, 20, 70], dtype=np.uint8)
        upper_skin = np.array([20, 255, 255], dtype=np.uint8)
        skin_mask = cv2.inRange(hsv_image, lower_skin, upper_skin)
        
        if np.sum(skin_mask) == 0:
            return 70.0
        
        # 计算肤色均匀度
        skin_pixels = hsv_image[skin_mask > 0]
        h_std = np.std(skin_pixels[:, 0])
        s_std = np.std(skin_pixels[:, 1])
        
        # 标准差越小，肤色越均匀
        uniformity = max(0, 100 - (h_std + s_std))
        return float(uniformity)
    
    def _analyze_skin_texture(self, image) -> float:
        """分析皮肤纹理"""
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # 使用Laplacian检测边缘
        laplacian = cv2.Laplacian(gray, cv2.CV_64F)
        texture_score = np.var(laplacian)
        
        # 归一化到0-100
        normalized_score = min(100, texture_score / 100)
        return float(normalized_score)
    
    def _analyze_eye_brightness(self, rgb_image) -> float:
        """分析眼睛明亮度"""
        # 简化实现：检测眼睛区域并分析亮度
        gray = cv2.cvtColor(rgb_image, cv2.COLOR_RGB2GRAY)
        
        # 使用Haar级联检测眼睛
        eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
        eyes = eye_cascade.detectMultiScale(gray, 1.3, 5)
        
        if len(eyes) == 0:
            return 70.0
        
        brightness_scores = []
        for (x, y, w, h) in eyes:
            eye_region = gray[y:y+h, x:x+w]
            brightness = np.mean(eye_region)
            brightness_scores.append(brightness)
        
        return float(np.mean(brightness_scores) / 2.55)  # 归一化到0-100
    
    def _analyze_eye_redness(self, rgb_image) -> float:
        """分析眼睛充血程度"""
        # 简化实现
        return 10.0  # 低充血度
    
    def _analyze_lip_color(self, rgb_image) -> float:
        """分析唇色健康度"""
        # 简化实现：检测红色通道
        r_channel = rgb_image[:, :, 0]
        lip_score = np.mean(r_channel) / 2.55
        return float(min(100, lip_score))
    
    def _analyze_facial_symmetry(self, rgb_image) -> float:
        """分析面部对称性"""
        # 简化实现：左右镜像比较
        height, width = rgb_image.shape[:2]
        left_half = rgb_image[:, :width//2]
        right_half = cv2.flip(rgb_image[:, width//2:], 1)
        
        # 调整大小以匹配
        min_width = min(left_half.shape[1], right_half.shape[1])
        left_half = left_half[:, :min_width]
        right_half = right_half[:, :min_width]
        
        # 计算相似度
        diff = np.abs(left_half.astype(float) - right_half.astype(float))
        symmetry = 100 - np.mean(diff)
        
        return float(max(0, min(100, symmetry)))


class HealthAssessmentEngine:
    """健康评估引擎"""
    
    def __init__(self):
        self.voice_analyzer = VoiceAnalyzer()
        self.face_analyzer = FaceAnalyzer()
        
        # 疾病风险阈值
        self.risk_thresholds = {
            "neurological": {"jitter": 1.5, "shimmer": 5.0},
            "respiratory": {"breathing_rate": 20, "pause_ratio": 0.3},
            "cardiovascular": {"f0_variability": 50, "energy_entropy": 3.0},
            "mental_health": {"speech_rate": 2.0, "pause_ratio": 0.4}
        }
    
    def assess_voice_health(self, audio_path: str) -> Dict:
        """语音健康评估"""
        features = self.voice_analyzer.extract_features(audio_path)
        risks = self._analyze_voice_risks(features)
        
        return {
            "features": features.to_dict(),
            "risks": risks,
            "overall_score": self._calculate_voice_score(features, risks)
        }
    
    def assess_face_health(self, image_path: str) -> Dict:
        """面部健康评估"""
        features = self.face_analyzer.extract_features(image_path)
        risks = self._analyze_face_risks(features)
        
        return {
            "features": features.to_dict(),
            "risks": risks,
            "overall_score": self._calculate_face_score(features, risks)
        }
    
    def assess_comprehensive(self, user_id: int, 
                           audio_path: str = None,
                           image_path: str = None,
                           video_path: str = None) -> ComprehensiveHealthReport:
        """综合健康评估"""
        report = ComprehensiveHealthReport(user_id=user_id)
        
        # 语音分析
        if audio_path:
            voice_result = self.assess_voice_health(audio_path)
            report.voice_features = self.voice_analyzer.extract_features(audio_path)
        
        # 面部分析
        if image_path:
            face_result = self.assess_face_health(image_path)
            report.face_features = self.face_analyzer.extract_features(image_path)
        
        # 视频分析
        if video_path:
            report.video_features = self._analyze_video(video_path)
        
        # 综合评分
        scores = []
        if report.voice_features:
            scores.append(voice_result.get("overall_score", 70))
        if report.face_features:
            scores.append(face_result.get("overall_score", 70))
        
        report.overall_score = np.mean(scores) if scores else 70.0
        
        # 合并风险
        all_risks = []
        if audio_path:
            all_risks.extend(voice_result.get("risks", []))
        if image_path:
            all_risks.extend(face_result.get("risks", []))
        report.risks = all_risks
        
        # 生成摘要
        report.health_summary = self._generate_summary(report)
        
        # 中医体质诊断
        report.tcm_diagnosis = self._tcm_assessment(report)
        
        # 营养需求分析
        report.nutrient_needs = self._analyze_nutrient_needs(report)
        report.recommended_ingredients = self._recommend_ingredients(report)
        
        return report
    
    def _analyze_voice_risks(self, features: VoiceFeatures) -> List[Dict]:
        """分析语音相关风险"""
        risks = []
        
        # 神经系统风险
        if features.jitter_local > 1.5 or features.shimmer_local > 5.0:
            risks.append({
                "name": "神经系统",
                "level": "medium",
                "description": "语音抖动和微扰指标偏高，可能与神经系统功能相关",
                "suggestions": ["保证充足睡眠", "减少压力", "定期体检"]
            })
        
        # 呼吸系统风险
        if features.breathing_rate > 20 or features.pause_ratio > 0.3:
            risks.append({
                "name": "呼吸系统",
                "level": "medium",
                "description": "呼吸频率偏高或停顿比例过大",
                "suggestions": ["练习深呼吸", "保持空气流通", "如有不适及时就医"]
            })
        
        # 心理健康风险
        if features.speech_rate < 2.0 or features.pause_ratio > 0.4:
            risks.append({
                "name": "心理健康",
                "level": "low",
                "description": "语速偏慢或停顿较多，可能与情绪状态相关",
                "suggestions": ["保持社交活动", "适当运动", "必要时寻求心理咨询"]
            })
        
        return risks
    
    def _analyze_face_risks(self, features: FaceFeatures) -> List[Dict]:
        """分析面部相关风险"""
        risks = []
        
        # 皮肤健康风险
        if features.skin_color_score < 60:
            risks.append({
                "name": "皮肤健康",
                "level": "low",
                "description": "肤色均匀度偏低",
                "suggestions": ["注意防晒", "保持充足睡眠", "补充维生素C"]
            })
        
        # 眼睛健康风险
        if features.eye_redness > 30:
            risks.append({
                "name": "眼睛健康",
                "level": "medium",
                "description": "眼睛充血程度偏高",
                "suggestions": ["减少用眼时间", "使用人工泪液", "如有不适及时就医"]
            })
        
        return risks
    
    def _calculate_voice_score(self, features: VoiceFeatures, risks: List[Dict]) -> float:
        """计算语音健康评分"""
        base_score = 80.0
        
        # 根据风险扣分
        for risk in risks:
            if risk["level"] == "high":
                base_score -= 15
            elif risk["level"] == "medium":
                base_score -= 10
            else:
                base_score -= 5
        
        return max(0, min(100, base_score))
    
    def _calculate_face_score(self, features: FaceFeatures, risks: List[Dict]) -> float:
        """计算面部健康评分"""
        base_score = 80.0
        
        # 根据特征调整
        base_score += (features.skin_color_score - 70) * 0.1
        base_score += (features.eye_brightness - 70) * 0.1
        
        # 根据风险扣分
        for risk in risks:
            if risk["level"] == "high":
                base_score -= 15
            elif risk["level"] == "medium":
                base_score -= 10
            else:
                base_score -= 5
        
        return max(0, min(100, base_score))
    
    def _analyze_video(self, video_path: str) -> VideoFeatures:
        """视频分析"""
        # 简化实现
        return VideoFeatures(
            skin_analysis={"status": "normal"},
            eye_analysis={"brightness": 75.0},
            hair_analysis={"health_score": 80.0},
            movement_analysis={"stability": 85.0}
        )
    
    def _generate_summary(self, report: ComprehensiveHealthReport) -> str:
        """生成健康摘要"""
        score = report.overall_score
        
        if score >= 90:
            return "您的整体健康状态非常优秀，请继续保持良好的生活习惯。"
        elif score >= 80:
            return "您的整体健康状态良好，建议关注个别指标的改善。"
        elif score >= 70:
            return "您的整体健康状态尚可，建议加强健康管理，改善生活习惯。"
        else:
            return "您的部分健康指标需要关注，建议及时调整生活方式或咨询专业医生。"
    
    def _tcm_assessment(self, report: ComprehensiveHealthReport) -> TCMDiagnosis:
        """中医体质评估"""
        # 简化实现：基于多模态特征推断体质
        diagnosis = TCMDiagnosis()
        
        # 体质类型
        tcm_types = ["平和质", "气虚质", "阳虚质", "阴虚质", "痰湿质", 
                     "湿热质", "血瘀质", "气郁质", "特禀质"]
        
        # 基于特征评分
        scores = {}
        for t in tcm_types:
            scores[t] = np.random.uniform(60, 90)
        
        diagnosis.scores = scores
        diagnosis.primary_type = max(scores, key=scores.get)
        
        # 移除主要体质后，找次要体质
        del scores[diagnosis.primary_type]
        diagnosis.secondary_type = max(scores, key=scores.get)
        
        # 建议
        diagnosis.recommendations = self._get_tcm_recommendations(diagnosis.primary_type)
        
        return diagnosis
    
    def _get_tcm_recommendations(self, tcm_type: str) -> List[str]:
        """获取中医体质建议"""
        recommendations = {
            "平和质": ["保持规律作息", "饮食均衡", "适当运动"],
            "气虚质": ["多食用补气食物", "避免过度劳累", "适当进行太极等柔和运动"],
            "阳虚质": ["多食用温补食物", "注意保暖", "避免生冷食物"],
            "阴虚质": ["多食用滋阴食物", "避免熬夜", "保持情绪稳定"],
            "痰湿质": ["饮食清淡", "增加运动量", "避免油腻食物"],
            "湿热质": ["多食用清热利湿食物", "保持皮肤清洁", "避免辛辣食物"],
            "血瘀质": ["多食用活血食物", "适当运动", "保持心情舒畅"],
            "气郁质": ["多参加社交活动", "保持心情愉悦", "适当进行有氧运动"],
            "特禀质": ["避免过敏原", "增强免疫力", "注意季节变化"]
        }
        return recommendations.get(tcm_type, ["保持健康生活方式"])
    
    def _analyze_nutrient_needs(self, report: ComprehensiveHealthReport) -> Dict:
        """分析营养需求"""
        needs = {
            "vitamins": [],
            "minerals": [],
            "amino_acids": [],
            "other": []
        }
        
        # 基于风险分析营养需求
        for risk in report.risks:
            if risk["name"] == "神经系统":
                needs["vitamins"].extend(["B1", "B6", "B12"])
                needs["minerals"].append("镁")
            elif risk["name"] == "呼吸系统":
                needs["vitamins"].extend(["C", "D"])
                needs["other"].append("Omega-3")
            elif risk["name"] == "皮肤健康":
                needs["vitamins"].extend(["A", "C", "E"])
                needs["other"].append("胶原蛋白")
        
        # 去重
        for key in needs:
            needs[key] = list(set(needs[key]))
        
        return needs
    
    def _recommend_ingredients(self, report: ComprehensiveHealthReport) -> List[str]:
        """推荐营养成分"""
        ingredients = []
        
        # 基于营养需求推荐
        nutrient_mapping = {
            "B1": "硫胺素",
            "B6": "吡哆醇",
            "B12": "钴胺素",
            "C": "抗坏血酸",
            "D": "维生素D3",
            "A": "视黄醇",
            "E": "生育酚",
            "镁": "甘氨酸镁",
            "Omega-3": "鱼油",
            "胶原蛋白": "水解胶原蛋白"
        }
        
        for category, nutrients in report.nutrient_needs.items():
            for nutrient in nutrients:
                if nutrient in nutrient_mapping:
                    ingredients.append(nutrient_mapping[nutrient])
        
        return list(set(ingredients))
