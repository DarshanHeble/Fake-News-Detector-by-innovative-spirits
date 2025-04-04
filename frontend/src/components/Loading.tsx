import { motion } from "framer-motion";
import "./Loading.css";

const Loading = () => {
  const dots = Array.from({ length: 6 });

  return (
    <div className="loading-container">
      <motion.div
        className="rotating-wrapper"
        animate={{ rotate: 360 }}
        transition={{
          repeat: Infinity,
          duration: 2,
          ease: "linear",
        }}
      >
        {dots.map((_, index) => (
          <div
            key={index}
            className="loading-dot"
            style={{
              transform: `rotate(${(360 / 6) * index}deg) translateY(-15px)`,
              backgroundColor: "white",
            }}
          />
        ))}
      </motion.div>
    </div>
  );
};

export default Loading;
