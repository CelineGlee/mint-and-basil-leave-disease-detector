import React from "react"; 
import { View, ActivityIndicator, Text, StyleSheet } from "react-native";
import { Stack } from "expo-router";

export default function LoadingScreen() { 
  return (
    <>
      <Stack.Screen options={{ headerShown: false }} />
      <View style={styles.container}> 
        <ActivityIndicator size="large" color="#4CAF50" /> 
        <Text style={styles.text}>Analyzing your plant...</Text> 
      </View> 
    </>
  ); 
} 

const styles = StyleSheet.create({ 
  container: { 
    flex: 1, 
    justifyContent: "center", 
    alignItems: "center", 
    backgroundColor: "#fff", 
  }, 
  text: { 
    marginTop: 20, 
    fontSize: 25, 
    color: "#333", 
  }, 
});